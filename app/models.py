import re
from pydantic import BaseModel, Field, field_validator


def _strip_html(v):
    if isinstance(v, str):
        return re.sub(r'<[^>]+>', '', v)
    return v


class EmergencyContact(BaseModel):
    name: str = ""
    relationship: str = ""
    phone: str = ""

    @field_validator('name', 'phone')
    @classmethod
    def sanitize(cls, v):
        return _strip_html(v)


class SocialHistory(BaseModel):
    smokingStatus: str = "never"
    alcoholUse: str = ""
    occupation: str = ""
    exerciseHabits: str = ""
    diet: str = ""


class ActiveCondition(BaseModel):
    condition: str
    diagnosedDate: str = ""
    diagnosedBy: str = ""
    severity: str = ""
    notes: str = ""
    status: str = "active"

    @field_validator('condition', 'notes')
    @classmethod
    def sanitize(cls, v):
        return _strip_html(v)


class PastCondition(BaseModel):
    condition: str
    diagnosedDate: str = ""
    resolvedDate: str = ""
    notes: str = ""

    @field_validator('condition', 'notes')
    @classmethod
    def sanitize(cls, v):
        return _strip_html(v)


class ActiveMedication(BaseModel):
    medication: str
    dosage: str = ""
    frequency: str = ""
    route: str = ""
    startedDate: str = ""
    prescribedBy: str = ""
    purpose: str = ""
    notes: str = ""
    status: str = "active"

    @field_validator('medication', 'purpose', 'notes')
    @classmethod
    def sanitize(cls, v):
        return _strip_html(v)


class PastMedication(BaseModel):
    medication: str
    dosage: str = ""
    frequency: str = ""
    startedDate: str = ""
    stoppedDate: str = ""
    reasonStopped: str = ""

    @field_validator('medication', 'reasonStopped')
    @classmethod
    def sanitize(cls, v):
        return _strip_html(v)


class Allergy(BaseModel):
    allergen: str
    reaction: str = ""
    severity: str = ""
    onsetDate: str = ""
    notes: str = ""

    @field_validator('allergen', 'reaction', 'notes')
    @classmethod
    def sanitize(cls, v):
        return _strip_html(v)


class FamilyMember(BaseModel):
    relative: str
    age: str = ""
    livingStatus: str = "alive"
    conditions: str = ""
    notes: str = ""

    @field_validator('relative', 'conditions', 'notes')
    @classmethod
    def sanitize(cls, v):
        return _strip_html(v)


class Prescription(BaseModel):
    medication: str
    dosage: str = ""
    frequency: str = ""
    quantity: str = ""
    refills: str = ""

    @field_validator('medication')
    @classmethod
    def sanitize(cls, v):
        return _strip_html(v)


class Vitals(BaseModel):
    bloodPressure: str = ""
    heartRate: str = ""
    temperature: str = ""
    weight: str = ""
    height: str = ""
    bmi: str = ""
    respiratoryRate: str = ""
    oxygenSat: str = ""
    glucose: str = ""


class Patient(BaseModel):
    patientId: str = Field(..., min_length=1, max_length=30)
    name: str = Field(..., min_length=1, max_length=200)
    dateOfBirth: str
    age: int = 0
    gender: str
    phone: str = ""
    email: str = ""
    address: str = ""
    emergencyContact: EmergencyContact = EmergencyContact()
    activeConditions: list[ActiveCondition] = []
    pastConditions: list[PastCondition] = []
    activeMedications: list[ActiveMedication] = []
    pastMedications: list[PastMedication] = []
    allergies: list[Allergy] = []
    familyHistory: list[FamilyMember] = []
    socialHistory: SocialHistory = SocialHistory()
    surgicalHistory: str = ""
    immunizations: str = ""
    generalNotes: str = ""
    visits: list = []
    labResults: list = []

    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v):
        if v not in ('male', 'female', 'other', 'unknown'):
            raise ValueError('gender must be male, female, other, or unknown')
        return v

    @field_validator('name', 'patientId', 'phone', 'email', 'address')
    @classmethod
    def sanitize_strings(cls, v):
        return _strip_html(v)


class Visit(BaseModel):
    date: str
    type: str = ""
    chiefComplaint: str = ""
    vitals: Vitals = Vitals()
    symptoms: str = ""
    examination: str = ""
    assessment: str = ""
    plan: str = ""
    prescriptions: list[Prescription] = []
    labsOrdered: str = ""
    notes: str = ""
    followUp: str = ""
    seenBy: str = ""

    @field_validator('chiefComplaint', 'symptoms', 'assessment', 'plan', 'notes')
    @classmethod
    def sanitize(cls, v):
        return _strip_html(v)


class Settings(BaseModel):
    ollama_model: str = "qwen2.5:4b"
    ollama_host: str = "http://localhost:11434"
    system_prompt: str = ""
    temperature: float = 0.7
    max_tokens: int = 2048

    @field_validator('temperature')
    @classmethod
    def validate_temperature(cls, v):
        if not 0.0 <= v <= 2.0:
            raise ValueError('temperature must be between 0.0 and 2.0')
        return v

    @field_validator('ollama_model', 'system_prompt')
    @classmethod
    def sanitize(cls, v):
        return _strip_html(v)
