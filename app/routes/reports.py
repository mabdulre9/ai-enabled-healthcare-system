import io
from datetime import datetime
from flask import Blueprint, jsonify, send_file
from app.auth import login_required
from app.data import get_patient
from app.services.reports import generate_visit_report_docx, generate_patient_report_docx

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/api/patients/<patient_id>/visits/<visit_id>/report', methods=['GET'])
@login_required
def api_generate_visit_report(patient_id, visit_id):
    patient = get_patient(patient_id)

    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    visit = None
    if patient.get('visits'):
        visit = next((v for v in patient['visits'] if v.get('visitId') == visit_id), None)

    if not visit:
        return jsonify({'error': 'Visit not found'}), 404

    try:
        doc = generate_visit_report_docx(patient, visit)
        file_stream = io.BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)

        filename = f"Visit_Report_{patient_id}_{visit_id}_{datetime.now().strftime('%Y%m%d')}.docx"

        return send_file(
            file_stream,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        return jsonify({'error': f'Error generating report: {str(e)}'}), 500


@reports_bp.route('/api/patients/<patient_id>/full-report', methods=['GET'])
@login_required
def api_generate_patient_report(patient_id):
    patient = get_patient(patient_id)

    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    try:
        doc = generate_patient_report_docx(patient)
        file_stream = io.BytesIO()
        doc.save(file_stream)
        file_stream.seek(0)

        patient_name = patient.get('name', 'Unknown').replace(' ', '_')
        filename = f"Complete_Medical_Record_{patient_id}_{patient_name}_{datetime.now().strftime('%Y%m%d')}.docx"

        return send_file(
            file_stream,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        return jsonify({'error': f'Error generating report: {str(e)}'}), 500
