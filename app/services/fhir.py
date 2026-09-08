from datetime import datetime


def convert_fhir_to_simplified(fhir_data):
    if 'patientId' in fhir_data and 'dateOfBirth' in fhir_data:
        return fhir_data

    if fhir_data.get('resourceType') == 'Bundle':
        patient_resource = None
        conditions = []
        medications = []
        allergies = []
        observations = []

        for entry in fhir_data.get('entry', []):
            resource = entry.get('resource', {})
            resource_type = resource.get('resourceType')

            if resource_type == 'Patient':
                patient_resource = resource
            elif resource_type == 'Condition':
                conditions.append(resource)
            elif resource_type in ['MedicationRequest', 'MedicationStatement']:
                medications.append(resource)
            elif resource_type == 'AllergyIntolerance':
                allergies.append(resource)
            elif resource_type == 'Observation':
                observations.append(resource)

        if not patient_resource:
            raise ValueError("No Patient resource found in Bundle")

        simplified = convert_fhir_patient(patient_resource)

        if conditions:
            simplified['activeConditions'] = [
                convert_fhir_condition(c) for c in conditions
                if c.get('clinicalStatus', {}).get('coding', [{}])[0].get('code') == 'active'
            ]
            simplified['pastConditions'] = [
                convert_fhir_condition(c) for c in conditions
                if c.get('clinicalStatus', {}).get('coding', [{}])[0].get('code') in ['resolved', 'inactive']
            ]

        if medications:
            simplified['activeMedications'] = [
                convert_fhir_medication(m) for m in medications
                if m.get('status') in ['active', 'intended']
            ]
            simplified['pastMedications'] = [
                convert_fhir_medication(m) for m in medications
                if m.get('status') in ['stopped', 'completed']
            ]

        if allergies:
            simplified['allergies'] = [convert_fhir_allergy(a) for a in allergies]

        return simplified

    elif fhir_data.get('resourceType') == 'Patient':
        return convert_fhir_patient(fhir_data)

    else:
        raise ValueError("Unsupported FHIR format. Expected Bundle or Patient resource.")


def convert_fhir_patient(patient):
    name = "Unknown"
    if patient.get('name') and len(patient['name']) > 0:
        name_obj = patient['name'][0]
        given = ' '.join(name_obj.get('given', []))
        family = name_obj.get('family', '')
        prefix = ' '.join(name_obj.get('prefix', []))
        name = f"{prefix} {given} {family}".strip()

    birth_date = patient.get('birthDate', '')

    age = 0
    if birth_date:
        today = datetime.now()
        birth = datetime.fromisoformat(birth_date)
        age = today.year - birth.year
        if today.month < birth.month or (today.month == birth.month and today.day < birth.day):
            age -= 1

    phone = ""
    if patient.get('telecom'):
        for contact in patient['telecom']:
            if contact.get('system') == 'phone':
                phone = contact.get('value', '')
                break

    email = ""
    if patient.get('telecom'):
        for contact in patient['telecom']:
            if contact.get('system') == 'email':
                email = contact.get('value', '')
                break

    address = ""
    if patient.get('address') and len(patient['address']) > 0:
        addr = patient['address'][0]
        line = ', '.join(addr.get('line', []))
        city = addr.get('city', '')
        state = addr.get('state', '')
        postal = addr.get('postalCode', '')
        address = f"{line}\n{city}, {state} {postal}".strip()

    fhir_id = str(patient.get('id', 'UNKNOWN'))
    if fhir_id.startswith('PATIENT-') and len(fhir_id) <= 30:
        patient_id = fhir_id
    else:
        patient_id = f"PATIENT-{fhir_id[:8]}"

    return {
        'patientId': patient_id,
        'name': name,
        'dateOfBirth': birth_date,
        'age': age,
        'gender': patient.get('gender', 'unknown'),
        'phone': phone,
        'email': email,
        'address': address,
        'emergencyContact': {'name': '', 'relationship': '', 'phone': ''},
        'activeConditions': [],
        'pastConditions': [],
        'activeMedications': [],
        'pastMedications': [],
        'allergies': [],
        'familyHistory': [],
        'socialHistory': {
            'smokingStatus': 'unknown',
            'alcoholUse': '',
            'occupation': '',
            'exerciseHabits': '',
            'diet': ''
        },
        'surgicalHistory': '',
        'immunizations': '',
        'generalNotes': f"Imported from FHIR Bundle. Original FHIR ID: {patient.get('id')}",
        'visits': [],
        'labResults': []
    }


def convert_fhir_condition(condition):
    condition_name = "Unknown Condition"
    if condition.get('code'):
        if condition['code'].get('text'):
            condition_name = condition['code']['text']
        elif condition['code'].get('coding') and len(condition['code']['coding']) > 0:
            condition_name = condition['code']['coding'][0].get('display', 'Unknown')

    onset_date = ""
    if condition.get('onsetDateTime'):
        onset_date = condition['onsetDateTime'].split('T')[0]
    elif condition.get('recordedDate'):
        onset_date = condition['recordedDate'].split('T')[0]

    return {
        'condition': condition_name,
        'diagnosedDate': onset_date,
        'diagnosedBy': '',
        'severity': '',
        'notes': f"FHIR ID: {condition.get('id', 'unknown')}",
        'status': 'active'
    }


def convert_fhir_medication(medication):
    med_name = "Unknown Medication"
    if medication.get('medicationCodeableConcept'):
        if medication['medicationCodeableConcept'].get('text'):
            med_name = medication['medicationCodeableConcept']['text']
        elif medication['medicationCodeableConcept'].get('coding'):
            med_name = medication['medicationCodeableConcept']['coding'][0].get('display', 'Unknown')

    dosage_text = ""
    if medication.get('dosageInstruction') and len(medication['dosageInstruction']) > 0:
        dosage_text = medication['dosageInstruction'][0].get('text', '')

    return {
        'medication': med_name,
        'dosage': '',
        'frequency': dosage_text,
        'route': 'oral',
        'startedDate': medication.get('authoredOn', '').split('T')[0] if medication.get('authoredOn') else '',
        'prescribedBy': '',
        'purpose': '',
        'notes': '',
        'status': 'active'
    }


def convert_fhir_allergy(allergy):
    allergen = "Unknown Allergen"
    if allergy.get('code'):
        if allergy['code'].get('text'):
            allergen = allergy['code']['text']
        elif allergy['code'].get('coding'):
            allergen = allergy['code']['coding'][0].get('display', 'Unknown')

    reaction = ""
    severity = "unknown"
    if allergy.get('reaction') and len(allergy['reaction']) > 0:
        reaction_obj = allergy['reaction'][0]
        if reaction_obj.get('manifestation'):
            manifestations = []
            for m in reaction_obj['manifestation']:
                if m.get('text'):
                    manifestations.append(m['text'])
                elif m.get('coding'):
                    manifestations.append(m['coding'][0].get('display', ''))
            reaction = ', '.join(manifestations)
        severity = reaction_obj.get('severity', 'unknown')

    return {
        'allergen': allergen,
        'reaction': reaction,
        'severity': severity,
        'onsetDate': allergy.get('recordedDate', '').split('T')[0] if allergy.get('recordedDate') else '',
        'notes': f"FHIR ID: {allergy.get('id', 'unknown')}"
    }
