def build_patient_context(patient):
    context = "PATIENT RECORD\n"
    context += "=" * 50 + "\n\n"

    context += f"Patient ID: {patient.get('patientId', 'N/A')}\n"
    context += f"Name: {patient.get('name', 'N/A')}\n"
    context += f"Age: {patient.get('age', 'N/A')} years old\n"
    context += f"Gender: {patient.get('gender', 'N/A')}\n"
    context += f"Date of Birth: {patient.get('dateOfBirth', 'N/A')}\n\n"

    if patient.get('activeConditions'):
        context += "ACTIVE CONDITIONS:\n"
        for cond in patient['activeConditions']:
            context += f"  - {cond.get('condition', 'N/A')} (diagnosed {cond.get('diagnosedDate', 'N/A')})\n"
            if cond.get('notes'):
                context += f"    Notes: {cond['notes']}\n"
        context += "\n"

    if patient.get('pastConditions'):
        context += "PAST CONDITIONS (RESOLVED):\n"
        for cond in patient['pastConditions']:
            context += f"  - {cond.get('condition', 'N/A')} ({cond.get('diagnosedDate', 'N/A')} to {cond.get('resolvedDate', 'N/A')})\n"
        context += "\n"

    if patient.get('activeMedications'):
        context += "CURRENT MEDICATIONS:\n"
        for med in patient['activeMedications']:
            context += f"  - {med.get('medication', 'N/A')} {med.get('dosage', '')} {med.get('frequency', '')}\n"
            if med.get('purpose'):
                context += f"    Purpose: {med['purpose']}\n"
        context += "\n"

    if patient.get('pastMedications'):
        context += "DISCONTINUED MEDICATIONS:\n"
        for med in patient['pastMedications']:
            context += f"  - {med.get('medication', 'N/A')} (stopped {med.get('stoppedDate', 'N/A')})\n"
            if med.get('reasonStopped'):
                context += f"    Reason: {med['reasonStopped']}\n"
        context += "\n"

    if patient.get('allergies'):
        context += "ALLERGIES:\n"
        for allergy in patient['allergies']:
            context += f"  - {allergy.get('allergen', 'N/A')} - {allergy.get('reaction', 'N/A')} ({allergy.get('severity', 'N/A')} severity)\n"
        context += "\n"

    if patient.get('familyHistory'):
        context += "FAMILY HISTORY:\n"
        for family in patient['familyHistory']:
            context += f"  {family.get('relative', 'N/A')} ({family.get('age', 'N/A')}, {family.get('livingStatus', 'N/A')}):\n"
            if family.get('conditions'):
                for cond in family['conditions']:
                    if isinstance(cond, str):
                        context += f"    - {cond}\n"
                    else:
                        context += f"    - {cond.get('condition', 'N/A')} (onset age {cond.get('ageOfOnset', 'N/A')})\n"
        context += "\n"

    if patient.get('socialHistory'):
        sh = patient['socialHistory']
        context += "SOCIAL HISTORY:\n"
        context += f"  Smoking: {sh.get('smokingStatus', 'N/A')}\n"
        context += f"  Alcohol: {sh.get('alcoholUse', 'N/A')}\n"
        context += f"  Occupation: {sh.get('occupation', 'N/A')}\n"
        context += f"  Exercise: {sh.get('exerciseHabits', 'N/A')}\n\n"

    if patient.get('visits'):
        context += "VISIT HISTORY:\n"
        recent_visits = patient['visits'][-5:]
        for visit in recent_visits:
            context += f"\n  Visit Date: {visit.get('date', 'N/A')}\n"
            context += f"  Type: {visit.get('type', 'N/A')}\n"
            context += f"  Chief Complaint: {visit.get('chiefComplaint', 'N/A')}\n"
            if visit.get('vitals'):
                vitals = visit['vitals']
                context += f"  Vitals: BP {vitals.get('bloodPressure', 'N/A')}, HR {vitals.get('heartRate', 'N/A')}, Temp {vitals.get('temperature', 'N/A')}\n"
            context += f"  Symptoms: {visit.get('symptoms', 'N/A')}\n"
            context += f"  Assessment: {visit.get('assessment', 'N/A')}\n"
            context += f"  Plan: {visit.get('plan', 'N/A')}\n"
        context += "\n"

    if patient.get('labResults'):
        context += "RECENT LAB RESULTS:\n"
        for lab in patient['labResults'][-5:]:
            context += f"  {lab.get('testName', 'N/A')} ({lab.get('date', 'N/A')}): {lab.get('result', 'N/A')}\n"
        context += "\n"

    return context
