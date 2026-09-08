from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.auth import login_required
from app.data import get_patient, upsert_patient, generate_visit_id
from app.models import Visit

visits_bp = Blueprint('visits', __name__)


def _validation_errors(e):
    return [
        {'loc': [str(x) for x in err.get('loc', [])], 'msg': err.get('msg', ''), 'type': err.get('type', '')}
        for err in e.errors()
    ]


@visits_bp.route('/api/patients/<patient_id>/visits', methods=['POST'])
@login_required
def api_add_visit(patient_id):
    visit_data = request.json
    try:
        visit = Visit(**visit_data)
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': _validation_errors(e)}), 400

    visit_dict = visit.model_dump()
    patient = get_patient(patient_id)

    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    if 'visits' not in patient or patient['visits'] is None:
        patient['visits'] = []

    visit_dict['visitId'] = generate_visit_id(patient_id)
    patient['visits'].append(visit_dict)
    upsert_patient(patient)

    return jsonify({'success': True, 'visitId': visit_dict['visitId']})
