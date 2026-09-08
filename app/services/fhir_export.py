import uuid
from datetime import datetime, timezone

CS_CLINICAL = 'http://terminology.hl7.org/CodeSystem/condition-clinical'
CS_VERIFICATION = 'http://terminology.hl7.org/CodeSystem/condition-ver-status'
CS_ALLERGY_CLINICAL = 'http://terminology.hl7.org/CodeSystem/allergyintolerance-clinical'
CS_ALLERGY_VERIFICATION = 'http://terminology.hl7.org/CodeSystem/allergyintolerance-verification'
ALLERGY_SEVERITIES = ('mild', 'moderate', 'severe')
GENDERS = ('male', 'female', 'other', 'unknown')


def _id_safe(patient_id):
    return patient_id if patient_id and len(patient_id) <= 64 else 'unknown'


def _datetime(date_str):
    if not date_str:
        return None
    return f'{date_str}T00:00:00Z' if len(date_str) == 10 else date_str


def _patient_resource(patient):
    pid = _id_safe(patient.get('patientId', ''))
    res = {
        'resourceType': 'Patient',
        'id': pid,
        'text': {'status': 'generated',
                 'div': f'<div xmlns="http://www.w3.org/1999/xhtml">{patient.get("name", "")}</div>'}
    }

    name = patient.get('name', '')
    parts = name.split(' ', 1)
    res['name'] = [{
        'use': 'official',
        'given': [parts[0]],
        'family': parts[1] if len(parts) > 1 else ''
    }]

    if patient.get('dateOfBirth'):
        res['birthDate'] = patient['dateOfBirth']

    gender = patient.get('gender', 'unknown')
    res['gender'] = gender if gender in GENDERS else 'unknown'

    telecom = []
    if patient.get('phone'):
        telecom.append({'system': 'phone', 'value': patient['phone']})
    if patient.get('email'):
        telecom.append({'system': 'email', 'value': patient['email']})
    if telecom:
        res['telecom'] = telecom

    if patient.get('address'):
        res['address'] = [{'line': [patient['address']]}]

    ec = patient.get('emergencyContact') or {}
    if ec.get('name'):
        contact = {'name': [{'use': 'official', 'text': ec['name']}],
                   'relationship': [{'text': ec.get('relationship', 'Emergency Contact')}]}
        if ec.get('phone'):
            contact['telecom'] = [{'system': 'phone', 'value': ec['phone']}]
        res['contact'] = [contact]

    return res


def _condition_resource(pid, cond, resolved):
    res = {
        'resourceType': 'Condition',
        'id': f'{pid}-condition-{uuid.uuid4().hex[:8]}',
        'clinicalStatus': {
            'coding': [{
                'system': CS_CLINICAL,
                'code': 'resolved' if resolved else 'active',
                'display': 'Resolved' if resolved else 'Active'
            }]
        },
        'verificationStatus': {
            'coding': [{
                'system': CS_VERIFICATION,
                'code': 'confirmed',
                'display': 'Confirmed'
            }]
        },
        'code': {'text': cond.get('condition', 'Unknown condition')},
        'subject': {'reference': f'Patient/{pid}'}
    }
    onset = _datetime(cond.get('diagnosedDate'))
    if onset:
        res['onsetDateTime'] = onset
    if resolved and cond.get('resolvedDate'):
        res['abatementDateTime'] = _datetime(cond['resolvedDate'])
    if cond.get('severity'):
        res['severity'] = {'text': cond['severity']}
    if cond.get('notes'):
        res['note'] = [{'text': cond['notes']}]
    return res


def _medication_request_resource(pid, med, stopped):
    res = {
        'resourceType': 'MedicationRequest',
        'id': f'{pid}-medication-{uuid.uuid4().hex[:8]}',
        'status': 'stopped' if stopped else 'active',
        'intent': 'plan',
        'medicationCodeableConcept': {'text': med.get('medication', 'Unknown medication')},
        'subject': {'reference': f'Patient/{pid}'}
    }
    dosage_parts = [med.get('dosage', ''), med.get('frequency', '')]
    dosage_text = ' '.join(p for p in dosage_parts if p)
    instruction = {}
    if dosage_text:
        instruction['text'] = dosage_text
    if med.get('route'):
        instruction['route'] = {'text': med['route']}
    if instruction:
        res['dosageInstruction'] = [instruction]
    authored = _datetime(med.get('startedDate'))
    if authored:
        res['authoredOn'] = authored
    if med.get('prescribedBy'):
        res['requester'] = {'display': med['prescribedBy']}
    if med.get('purpose'):
        res['reasonCode'] = [{'text': med['purpose']}]
    if med.get('notes'):
        res['note'] = [{'text': med['notes']}]
    if stopped and med.get('stoppedDate'):
        res['statusReason'] = {'text': f'Stopped {med["stoppedDate"]}'}
    if med.get('reasonStopped'):
        res['note'] = res.get('note', []) + [{'text': f'Reason stopped: {med["reasonStopped"]}'}]
    return res


def _allergy_resource(pid, allergy):
    res = {
        'resourceType': 'AllergyIntolerance',
        'id': f'{pid}-allergy-{uuid.uuid4().hex[:8]}',
        'clinicalStatus': {
            'coding': [{
                'system': CS_ALLERGY_CLINICAL,
                'code': 'active',
                'display': 'Active'
            }]
        },
        'verificationStatus': {
            'coding': [{
                'system': CS_ALLERGY_VERIFICATION,
                'code': 'confirmed',
                'display': 'Confirmed'
            }]
        },
        'code': {'text': allergy.get('allergen', 'Unknown allergen')},
        'patient': {'reference': f'Patient/{pid}'}
    }
    onset = _datetime(allergy.get('onsetDate'))
    if onset:
        res['onsetDateTime'] = onset
    recorded = _datetime(allergy.get('onsetDate'))
    if recorded:
        res['recordedDate'] = recorded
    severity = allergy.get('severity', '')
    if severity and severity.lower() in ALLERGY_SEVERITIES and (allergy.get('reaction') or allergy.get('notes')):
        reaction = {}
        if allergy.get('reaction'):
            reaction['manifestation'] = [{'text': allergy['reaction']}]
        reaction['severity'] = severity.lower()
        res['reaction'] = [reaction]
    elif allergy.get('reaction'):
        res['reaction'] = [{'manifestation': [{'text': allergy['reaction']}]}]
    if allergy.get('notes'):
        res['comment'] = allergy['notes']
    return res


def patient_to_fhir_bundle(patient):
    pid = _id_safe(patient.get('patientId', ''))
    entries = [{'fullUrl': f'urn:uuid:{uuid.uuid4()}', 'resource': _patient_resource(patient)}]

    for cond in patient.get('activeConditions') or []:
        entries.append({'fullUrl': f'urn:uuid:{uuid.uuid4()}',
                        'resource': _condition_resource(pid, cond, resolved=False)})
    for cond in patient.get('pastConditions') or []:
        entries.append({'fullUrl': f'urn:uuid:{uuid.uuid4()}',
                        'resource': _condition_resource(pid, cond, resolved=True)})
    for med in patient.get('activeMedications') or []:
        entries.append({'fullUrl': f'urn:uuid:{uuid.uuid4()}',
                        'resource': _medication_request_resource(pid, med, stopped=False)})
    for med in patient.get('pastMedications') or []:
        entries.append({'fullUrl': f'urn:uuid:{uuid.uuid4()}',
                        'resource': _medication_request_resource(pid, med, stopped=True)})
    for allergy in patient.get('allergies') or []:
        entries.append({'fullUrl': f'urn:uuid:{uuid.uuid4()}',
                        'resource': _allergy_resource(pid, allergy)})

    return {
        'resourceType': 'Bundle',
        'id': f'{pid}-bundle',
        'type': 'collection',
        'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'entry': entries
    }
