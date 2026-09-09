# AI-Enabled Healthcare Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/) 
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/) 
[![Ollama](https://img.shields.io/badge/AI-Ollama%20(Offline)-purple)](https://ollama.com) 
[![Documentation](https://img.shields.io/badge/Docs-available-blue)](https://mabdulre9.github.io/ai-enabled-healthcare-system/)

> **Local-First Electronic Medical Records (EMR) with an Offline AI Assistant**  
> 📖 **Documentation:** https://mabdulre9.github.io/ai-enabled-healthcare-system/

A privacy-first healthcare management system featuring offline AI powered by Ollama.
No cloud APIs and no data processors are used at runtime — all patient data stays on the machine running the app. For the at-rest caveats that come with local storage, see [Security & Compliance Notes](#security--compliance-notes).

![Runs Offline](https://img.shields.io/badge/ai-local%20only-brightgreen) 

---
## Key Features

### Complete EMR System

- **Patient Management**
  - Registration, demographics, contact information
- **Visit Tracking**
  - Consultations, diagnoses, treatment plans
- **Medical History**
  - Active conditions, medications, allergies, family history
- **Vital Signs**
  - Blood pressure, heart rate, temperature, BMI tracking
- **Lab Orders**
  - Tests-ordered text captured per visit and shown on reports (no structured lab-results entry or trending UI)
- **Immunizations**
  - Vaccination records management

### Offline AI Clinical Assistant

- **Local-First** - No runtime network calls; all data stays on your computer (stored unencrypted - see Security Notes)
- **Completely Offline** - No internet required for AI after the model download
- **Typewriter Display** - Responses revealed word-by-word (computed locally in one pass by Ollama)
- **Context-Aware** - Sends a structured summary of the record (most recent visits and labs included, not the full history) as the LLM prompt
- **Memory Management** - Frees RAM by restarting the Ollama server (force-stops the process; all models unload)
- **Clinical Q&A on Patient Context** - Free-text LLM chat over the record; the model may suggest differential diagnoses, flag interactions, or recommend treatments in prose, but there is no validated drug-interaction database or rules engine behind it and output can be wrong
- **Zero Cost** - Self hosted, no subscriptions

### Report Generator

- **Word Reports** - Medical reports with clinic letterhead
- **Complete Records** - Full patient history export
- **On Visit** - Single visit history export
- **One-Click Generation** - Instant .docx documents

### FHIR Integration

- **Import FHIR R4** - Ingest FHIR Bundle or Patient resources (e.g., Synthea exports)
- **Export FHIR R4** - Download any patient record as a FHIR collection Bundle
- **Data Validation** - Required fields and value checks on import

*Scope note: import/export use a simplified field mapping (Patient, Condition,
MedicationRequest/MedicationStatement, AllergyIntolerance; coded values are stored as
display text, Observations not yet converted). This is a FHIR data-exchange feature,
not a FHIR-conformant server: there is no RESTful FHIR API or CapabilityStatement.*

---

## System Architecture

The system follows a modern layered architecture for scalability, maintainability, and complete offline operation:

![System Architecture](assets/architecture.svg)

### Architecture Overview

- **Presentation Layer**: HTML5, CSS3, and vanilla JavaScript for responsive UI
- **Application Layer**: Flask 3.0.0 backend handling business logic and routing
- **AI Layer**: Ollama integration for completely offline AI assistance
- **Data Layer**: SQLite local database with privacy-first design
- **Integration Layer**: FHIR R4 data exchange (simplified Bundle import/export)

---

## Quick Start

### Prerequisites

- Python 3.12 or higher
- Ollama (for AI features)

### Installation

```bash
# 1. Clone or download this repository
cd healthcare-management-system

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python app.py

# 6. Open http://localhost:5000 in your browser and log in.
#    Default password: clinic123  (CHANGE IT before real use)
#    Set your own:    CLINIC_PASSWORD=your-secret python app.py
```


---

## Ollama AI Setup

### Step 1: Install Ollama

**Download from:** https://ollama.com/download

- **Windows:** Download installer, run, done
- **macOS:** Download .dmg, install
- **Linux:** `curl -fsSL https://ollama.com/install.sh | sh`

### Step 2: Download a Model

```bash
# Choose any model for example:

# Small & Fast (523MB) - Good for testing
ollama pull qwen3:0.6b

# Balanced (2.5GB) - Best overall
ollama pull qwen2.5:4b

# High Quality (2GB) - More accurate
ollama pull llama3.2:3b

# Check downloaded models
ollama list
```

### Step 3: Configure in System

1. Go to **Settings**
2. Enter model name (e.g., `qwen2.5:4b`)
3. Click **TEST MODEL** to verify
4. Click **SAVE SETTINGS**
5. Use AI Assistant - completely private

---

## Why This System?

### Complete Privacy

- **Local-Only Storage** - No cloud APIs; data is written only to your machine
- **Access Gate** - All pages and APIs require the shared login (see Security Notes)
- **Offline Capable** - Works without internet (after the one-time model download)

### Zero Cost

- **Free Software** - Open source, no licenses
- **Free AI** - Ollama is completely free
- **No Subscriptions** - No monthly fees ever
- **No Hidden Costs** - Everything is free

### Full Control

- **Self-Hosted** - Run on your own hardware
- **Customizable** - Modify to your needs
- **No Vendor Lock-in** - Your data, your control
- **Open Standards** - FHIR R4 data import/export

---

## Security & Compliance Notes

**This software is not "HIPAA-compliant" and no product can be.** Under the HIPAA Security
Rule, compliance is the responsibility of the covered entity (your clinic), achieved through
policies and safeguards. Being local-only reduces risk but does not satisfy the rule. Be
aware of what this app does and does not provide:

**Implemented:**
- All pages and API endpoints require authentication (session cookie)
- Server binds to `127.0.0.1` by default; debug mode off unless `FLASK_DEBUG=1`
- Input validation and HTML stripping on patient data (XSS mitigation)
- SQLite with transactions (protection against file corruption)

**Not implemented (you must compensate):**
- **Unique user accounts** - one shared password; the Security Rule requires per-user identification
- **Audit log** - no record of who viewed, changed, or deleted what
- **Encryption at rest** - the database and downloaded reports (Word/JSON/FHIR) are plain files; encrypt the disk (e.g., BitLocker/FileVault) and control PC access
- **Automatic logoff** - the session stays valid until the browser closes
- **Backup / recovery procedures** - copy `data/` regularly; patient deletion is permanent

For real clinical use you also need: locked workstations, trained staff, consent handling,
and a breach response plan. Do not use the default password.

---

## Use Cases

- **Small Clinics** - Affordable EMR without subscriptions
- **Solo Practitioners** - Complete patient management
- **Medical Education** - Safe learning environment
- **Clinical Research** - Structured data collection
- **Remote Healthcare** - Works completely offline
- **Home Health** - Portable, no connectivity needed

---

## Tech Stack

- **Backend:** Python Flask 3.0.0
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **AI:** Ollama (100% offline)
- **Documents:** python-docx
- **Standards:** FHIR R4 import/export (simplified mapping)
- **Accessibility:** Semantic HTML with `lang` set; form labels are not yet programmatically associated with inputs and ARIA attributes are absent, so the UI is **not** WCAG-conformant at any level

---

## System Requirements

- **OS:** Windows 10+, macOS, or Linux
- **Python:** 3.12 or higher
- **RAM:** 8GB minimum (16GB+ recommended for AI)
- **Storage:** Depends on LLM
- **Internet:** Only for initial download

---

## Configuration

Edit clinic information in `app/config.py` (lines 7-10):

```python
CLINIC_NAME = 'Your Clinic Name'
CLINIC_ADDRESS = '123 Medical Center Dr'
CLINIC_PHONE = '(555) 123-4567'
CLINIC_EMAIL = 'contact@clinic.com'
```

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch
3. Make your changes
4. Submit pull request

---

## License

MIT License - see [LICENSE](LICENSE) file

---

## Acknowledgments

- **Ollama** - For making local AI accessible and free
- **FHIR Community** - For healthcare interoperability standards
- **Flask** - For the excellent web framework

---

## Support

For issues or questions:

- **GitHub Issues:** Report bugs or request features
- **Documentation:** Check built-in docs at /docs
- **Troubleshooting:** See TROUBLESHOOTING.md

---

**Built with ❤️ for healthcare professionals**

**Local-first • Free & open source • Runs offline**

[⭐ Star this repo](https://github.com/mabdulre9/healthcare-system) if you find it useful!

---

## Feedback & Issues

If you encounter any bugs, have suggestions, or ideas for improvement, don’t hesitate to reach out at **mabdulre9@gmail.com** or open an issue on GitHub.

Contributions and feedback are always welcome!
