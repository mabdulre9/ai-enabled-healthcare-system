# FHIR R4 IMPORT & EXPORT GUIDE

## Now Supporting Real FHIR R4 Data!

The healthcare system now supports importing **actual FHIR R4 data** from sources like Synthea, hospital EHRs, and other FHIR-compliant systems.

---

## Supported Formats

### 1. FHIR R4 Bundle (Recommended)
Complete patient records with all resources bundled together.

**Example from Synthea:**
```json
{
  "resourceType": "Bundle",
  "type": "transaction",
  "entry": [
    {
      "resource": {
        "resourceType": "Patient",
        "id": "6ea8365d-e53f-2d4b-23b4-8eb3d83bd2cb",
        "name": [{"family": "Koelpin146", "given": ["Harry448"]}],
        "birthDate": "1997-07-19",
        "gender": "male"
      }
    },
    {
      "resource": {
        "resourceType": "Condition",
        ...
      }
    }
  ]
}
```

### 2. FHIR R4 Patient Resource
Single patient resource.

**Example:**
```json
{
  "resourceType": "Patient",
  "id": "example-id",
  "name": [{"family": "Doe", "given": ["Jane"]}],
  "birthDate": "1990-08-22",
  "gender": "female"
}
```

### 3. Simplified Format
Our custom simplified format (still supported).

**Example:**
```json
{
  "patientId": "PATIENT-001",
  "name": "Jane Doe",
  "dateOfBirth": "1990-08-22",
  "age": 34,
  "gender": "female"
}
```

---

## What Gets Converted

### From FHIR Patient Resource

| FHIR Field | Converted To |
|------------|-------------|
| `id` | `patientId` (prefixed with "PATIENT-") |
| `name[0].given + name[0].family` | `name` (full name as string) |
| `birthDate` | `dateOfBirth` |
| Auto-calculated from birthDate | `age` |
| `gender` | `gender` |
| `telecom[].value` (phone) | `phone` |
| `telecom[].value` (email) | `email` |
| `address[0]` | `address` (formatted string) |

### From FHIR Bundle Resources

| FHIR Resource | Converted To |
|---------------|-------------|
| `Patient` | Patient demographics |
| `Condition` (active) | `activeConditions[]` |
| `Condition` (resolved/inactive) | `pastConditions[]` |
| `MedicationRequest` (active) | `activeMedications[]` |
| `MedicationRequest` (stopped) | `pastMedications[]` |
| `AllergyIntolerance` | `allergies[]` |
| `Observation` | Future: Lab results |

---

## How to Import FHIR Data

### Step 1: Get FHIR Data

**From Synthea:**
1. Go to https://synthetichealth.github.io/synthea/
2. Download the Synthea generator
3. Run: `java -jar synthea.jar`
4. Find generated FHIR files in `output/fhir/`

**From Hospital EHR:**
- Request FHIR R4 export
- Usually provided as Bundle JSON

**From SMART on FHIR:**
- Use FHIR API to fetch patient data
- GET `/Patient/{id}/$everything`

### Step 2: Import into System

1. Open the healthcare system dashboard
2. Click **IMPORT PATIENT JSON**
3. Select your FHIR Bundle or Patient JSON file
4. System automatically detects format and converts
5. Confirmation message shows successful import

---

## Example: Importing Synthea Data

### What You Have (Synthea Output):
```
Harry448 Koelpin146 (Male, DOB: 1997-07-19)
- Phone: 555-719-4698
- Address: 758 Kirlin Light Unit 36, Clinton, MA 01510
```

### What Gets Created in System:
```
PATIENT-6ea8365d
Mr. Harry448 Koelpin146
Age: 27 (calculated)
Gender: male
Phone: 555-719-4698
Address: 758 Kirlin Light Unit 36
         Clinton, MA 01510
```

Plus all conditions, medications, and allergies from the Bundle!

---

## Conversion Details

### Name Conversion
FHIR:
```json
"name": [{
  "use": "official",
  "prefix": ["Mr."],
  "given": ["Harry448"],
  "family": "Koelpin146"
}]
```

Simplified:
```json
"name": "Mr. Harry448 Koelpin146"
```

### Address Conversion
FHIR:
```json
"address": [{
  "line": ["758 Kirlin Light Unit 36"],
  "city": "Clinton",
  "state": "MA",
  "postalCode": "01510"
}]
```

Simplified:
```json
"address": "758 Kirlin Light Unit 36\nClinton, MA 01510"
```

### Condition Conversion
FHIR:
```json
{
  "resourceType": "Condition",
  "code": {
    "coding": [{
      "system": "http://snomed.info/sct",
      "code": "44054006",
      "display": "Diabetes mellitus type 2"
    }]
  },
  "onsetDateTime": "2020-03-15",
  "clinicalStatus": {
    "coding": [{
      "code": "active"
    }]
  }
}
```

Simplified:
```json
{
  "condition": "Diabetes mellitus type 2",
  "diagnosedDate": "2020-03-15",
  "status": "active"
}
```

---

## Field Mapping Table

### Patient Demographics

| FHIR R4 Path | Our System Field | Notes |
|--------------|------------------|-------|
| `Patient.id` | `patientId` | Prefixed with "PATIENT-" |
| `Patient.name[0].prefix + given + family` | `name` | Concatenated |
| `Patient.birthDate` | `dateOfBirth` | ISO date format |
| Calculated | `age` | Auto-calculated from birthDate |
| `Patient.gender` | `gender` | As-is |
| `Patient.telecom[system=phone].value` | `phone` | First phone found |
| `Patient.telecom[system=email].value` | `email` | First email found |
| `Patient.address[0]` | `address` | Formatted as multi-line string |

### Conditions

| FHIR R4 Path | Our System Field |
|--------------|------------------|
| `Condition.code.text` or `code.coding[0].display` | `condition` |
| `Condition.onsetDateTime` or `recordedDate` | `diagnosedDate` |
| `Condition.clinicalStatus.coding[0].code` | Used to determine active vs past |

### Medications

| FHIR R4 Path | Our System Field |
|--------------|------------------|
| `MedicationRequest.medicationCodeableConcept.text` | `medication` |
| `MedicationRequest.dosageInstruction[0].text` | `frequency` |
| `MedicationRequest.authoredOn` | `startedDate` |
| `MedicationRequest.status` | Used to determine active vs past |

### Allergies

| FHIR R4 Path | Our System Field |
|--------------|------------------|
| `AllergyIntolerance.code.text` | `allergen` |
| `AllergyIntolerance.reaction[0].manifestation` | `reaction` |
| `AllergyIntolerance.reaction[0].severity` | `severity` |

---

## Exporting FHIR R4 Data

Every patient record can be exported as a **FHIR R4 collection Bundle**:

- **UI:** Patient Record → `DOWNLOAD FHIR` button
- **API:** `GET /api/patients/<patientId>/fhir-export` (returns `application/fhir+json`, downloads as `<patientId>_fhir.json`)

### What the Bundle Contains

| Simplified Field | FHIR Resource |
|---|---|
| Demographics, contact, emergency contact | `Patient` |
| activeConditions | `Condition` (clinicalStatus: active) |
| pastConditions | `Condition` (clinicalStatus: resolved) |
| activeMedications | `MedicationRequest` (status: active) |
| pastMedications | `MedicationRequest` (status: stopped) |
| allergies | `AllergyIntolerance` |

### Example Export (truncated)

```json
{
  "resourceType": "Bundle",
  "type": "collection",
  "timestamp": "2026-09-09T12:00:00Z",
  "entry": [
    { "resource": { "resourceType": "Patient", "id": "PATIENT-001", "gender": "female", "birthDate": "1990-08-22" } },
    { "resource": { "resourceType": "Condition", "clinicalStatus": { "coding": [{ "system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active" }] }, "code": { "text": "Type 2 Diabetes Mellitus" }, "subject": { "reference": "Patient/PATIENT-001" } } }
  ]
}
```

### Export Limitations (be honest with receiving systems)

- Coded values (SNOMED CT / LOINC / RxNorm) are **not** preserved from import — resources carry free-text `code.text` only
- Visits, vitals, and lab results are not exported (no Observation/Encounter resources)
- Gender, dates, and severity values are mapped to FHIR code sets where possible
- This makes the system suitable for **data handoff demos and backups**, not certified interoperability

---

## Limitations & Notes

### Current Limitations
- Observations not yet converted (planned for future)
- Encounters not yet converted (planned for future)
- Procedures not yet converted (planned for future)
- Family history not extracted from Bundle (requires additional resources)

### What's Preserved
- Original FHIR ID saved in notes
- Patient can be re-exported as a FHIR R4 collection Bundle (`DOWNLOAD FHIR` on the patient record, or `GET /api/patients/<id>/fhir-export`)
- Round-trip works for core fields: FHIR → simplified → FHIR (lossy: coded values like SNOMED/LOINC are stored as display text only)

### ID Generation
- External FHIR IDs become `PATIENT-{first-8-chars-of-fhir-id}`
- Original FHIR ID saved in `generalNotes`
- Example: FHIR ID `6ea8365d-e53f-2d4b-23b4-8eb3d83bd2cb` → `PATIENT-6ea8365d`
- IDs already in this system's format (`PATIENT-001`) are preserved on import, so exported Bundles re-import to the same record

### ⚠ Round-Trip Warning
Re-importing an exported Bundle **replaces** the patient record. Since visits, vitals,
and lab results are not part of the Bundle, they are **lost** on re-import.
Do not use FHIR re-import to "update" a record that has visit history.

---

## Error Messages

### "Unsupported FHIR format"
**Cause:** File is not a valid FHIR Bundle or Patient resource
**Fix:** Ensure file has `"resourceType": "Bundle"` or `"resourceType": "Patient"`

### "No Patient resource found in Bundle"
**Cause:** Bundle doesn't contain a Patient resource
**Fix:** Ensure Bundle has at least one Patient entry

### "INVALID JSON FILE"
**Cause:** File is not valid JSON
**Fix:** Validate JSON format, check for syntax errors

---

## Testing the Import

### Test with Synthea Data:

1. **Generate test data:**
   ```bash
   java -jar synthea.jar -p 1
   ```

2. **Find the file:**
   ```
   output/fhir/[patient-name].json
   ```

3. **Import:**
   - Dashboard → IMPORT PATIENT JSON
   - Select the file
   - Confirm conversion message
   - View imported patient

---

## Best Practices

### Before Importing:
1. **Validate** the FHIR data (use online validators)
2. **Backup** your current patient database
3. **Test** with one patient first
4. **Review** converted data after import

### After Importing:
1. **Verify** patient demographics
2. **Check** conditions and medications
3. **Add** any missing information manually
4. **Export** to create a backup in simplified format

### For Production:
1. **Map** organizational codes to your terminology
2. **Standardize** provider names and identifiers
3. **Validate** against your data quality rules
4. **Audit** imported records

---

## Round-Trip Compatibility

### FHIR → System → FHIR

**Import FHIR Bundle:**
```json
{
  "resourceType": "Bundle",
  "entry": [{"resource": {"resourceType": "Patient", ...}}]
}
```

**Converted to Simplified:**
```json
{
  "patientId": "PATIENT-abc123",
  "name": "John Doe",
  ...
}
```

**Re-exported as FHIR (DOWNLOAD FHIR):**
```json
{
  "resourceType": "Bundle",
  "type": "collection",
  "entry": [
    { "resource": { "resourceType": "Patient", "id": "PATIENT-abc123", ... } },
    { "resource": { "resourceType": "Condition", ... } }
  ]
}
```

The JSON export can be re-imported into this system; the FHIR Bundle can be consumed by FHIR-aware tools (with the coding limitations above).

---

## Common Synthea Scenarios

### Scenario 1: Import Single Patient
- File: `Harry448_Koelpin146_6ea8365d.json`
- Contains: Complete medical history
- Result: One patient with all conditions, meds, allergies

### Scenario 2: Import Multiple Patients
- Import files one at a time
- Each creates separate patient record
- No bulk import yet (coming in v2.1)

### Scenario 3: Update Existing Patient
- Import will detect existing ID
- Prompt to replace or cancel
- Choose replace to update with new data

---

## Future Enhancements

**Planned for v2.1:**
- Observation → Lab Results conversion
- Encounter → Visit Records conversion
- Procedure → Surgical History conversion
- DiagnosticReport → Lab Results
- Immunization → Immunizations list
- FamilyMemberHistory → Family History

---

## Support & Resources

### FHIR Resources:
- FHIR R4 Spec: https://hl7.org/fhir/R4/
- Synthea: https://synthetichealth.github.io/synthea/
- FHIR Validators: https://confluence.hl7.org/display/FHIR/Public+Test+Servers

### System Documentation:
- NEW_FEATURES.md - Feature guide
- README.md - Main documentation
- CHANGELOG.md - Version history

---

**Ready to import real FHIR data!** 🎉

The system now bridges the gap between:
- Real-world FHIR R4 standards
- Simplified clinical workflow
- Easy-to-use interface

Try importing a Synthea patient today!
