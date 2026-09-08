import json

from flask import Blueprint, request, jsonify, Response
from pydantic import ValidationError
from app.auth import login_required
from app.data import (
    list_patients, get_patient, patient_exists,
    upsert_patient, delete_patient, generate_patient_id
)
from app.models import Patient
from app.services.fhir import convert_fhir_to_simplified
from app.services.fhir_export import patient_to_fhir_bundle


def _validation_errors(e):
    return [
        {'loc': [str(x) for x in err.get('loc', [])], 'msg': err.get('msg', ''), 'type': err.get('type', '')}
        for err in e.errors()
    ]


patients_bp = Blueprint('patients', __name__)


@patients_bp.route('/api/generate-patient-id', methods=['GET'])
@login_required
def api_generate_patient_id():
    return jsonify({'patientId': generate_patient_id()})


@patients_bp.route('/api/patients', methods=['GET'])
@login_required
def api_get_patients():
    return jsonify(list_patients())


@patients_bp.route('/api/patients/<patient_id>', methods=['GET'])
@login_required
def api_get_patient(patient_id):
    patient = get_patient(patient_id)
    if patient:
        return jsonify(patient)
    return jsonify({'error': 'Patient not found'}), 404


@patients_bp.route('/api/patients/search', methods=['POST'])
@login_required
def api_search_patients():
    data = request.json
    search_term = data.get('searchTerm', '').lower()
    results = [
        p for p in list_patients()
        if search_term in p.get('patientId', '').lower() or
           search_term in p.get('name', '').lower()
    ]
    return jsonify(results)


@patients_bp.route('/api/patients', methods=['POST'])
@login_required
def api_create_patient():
    patient_data = request.json
    try:
        patient = Patient(**patient_data)
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': _validation_errors(e)}), 400

    patient_dict = patient.model_dump()

    if patient_exists(patient_dict['patientId']):
        return jsonify({'error': 'Patient ID already exists'}), 400

    upsert_patient(patient_dict)
    return jsonify({'success': True, 'patientId': patient_dict['patientId']})


@patients_bp.route('/api/patients/<patient_id>', methods=['PUT'])
@login_required
def api_update_patient(patient_id):
    patient_data = request.json
    try:
        patient = Patient(**patient_data)
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': _validation_errors(e)}), 400

    patient_dict = patient.model_dump()
    patient_dict['patientId'] = patient_id

    if not patient_exists(patient_id):
        return jsonify({'error': 'Patient not found'}), 404

    upsert_patient(patient_dict)
    return jsonify({'success': True})


@patients_bp.route('/api/patients/<patient_id>', methods=['DELETE'])
@login_required
def api_delete_patient(patient_id):
    delete_patient(patient_id)
    return jsonify({'success': True})


@patients_bp.route('/api/patients/<patient_id>/export', methods=['GET'])
@login_required
def api_export_patient(patient_id):
    patient = get_patient(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    return jsonify(patient)


@patients_bp.route('/api/patients/<patient_id>/fhir-export', methods=['GET'])
@login_required
def api_export_patient_fhir(patient_id):
    patient = get_patient(patient_id)
    if not patient:
        return jsonify({'error': 'Patient not found'}), 404
    bundle = patient_to_fhir_bundle(patient)
    response = Response(json.dumps(bundle, indent=2), mimetype='application/fhir+json')
    response.headers['Content-Disposition'] = f'attachment; filename="{patient_id}_fhir.json"'
    return response


@patients_bp.route('/api/patients/import', methods=['POST'])
@login_required
def api_import_patient():
    patient_data = request.json
    try:
        patient_data = convert_fhir_to_simplified(patient_data)
        patient = Patient(**patient_data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': _validation_errors(e)}), 400

    patient_dict = patient.model_dump()

    if patient_exists(patient_dict['patientId']):
        return jsonify({'error': 'Patient ID already exists', 'exists': True, 'patientId': patient_dict['patientId']}), 409

    upsert_patient(patient_dict)
    return jsonify({'success': True, 'patientId': patient_dict['patientId']})


@patients_bp.route('/api/patients/import/replace', methods=['POST'])
@login_required
def api_import_patient_replace():
    patient_data = request.json
    try:
        patient_data = convert_fhir_to_simplified(patient_data)
        patient = Patient(**patient_data)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': _validation_errors(e)}), 400

    patient_dict = patient.model_dump()
    upsert_patient(patient_dict)
    return jsonify({'success': True, 'patientId': patient_dict['patientId']})
