import os

DATA_FILE = os.path.join('data', 'patients.json')
SETTINGS_FILE = os.path.join('data', 'settings.json')
DATABASE_FILE = os.path.join('data', 'healthcare.db')

CLINIC_NAME = 'Neighborhood Clinic'
CLINIC_ADDRESS = '123 Medical Center Dr, City, State 12345'
CLINIC_PHONE = '(555) 123-4567'
CLINIC_EMAIL = 'contact@neighborhoodclinic.com'

OLLAMA_SETTINGS = {
    'ollama_model': 'qwen2.5:4b',
    'ollama_host': 'http://localhost:11434',
    'system_prompt': 'You are a clinical AI assistant. Provide evidence-based medical insights.',
    'temperature': 0.7,
    'max_tokens': 2048
}

CLINIC_PASSWORD = os.environ.get('CLINIC_PASSWORD', 'clinic123')
