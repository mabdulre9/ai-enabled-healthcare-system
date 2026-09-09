---
layout: default
title: Overview
---

# Healthcare Management System

A comprehensive, privacy-first healthcare management system featuring completely offline AI powered by Ollama.

## Introduction

Healthcare Management System is an Electronic Medical Records (EMR) application with an
integrated local AI assistant. It covers patient management, clinical documentation, and
AI-assisted Q&A over a patient's record. It is **not** a certified/validated clinical
decision-support system: AI output is free-text model generation and must be reviewed by a clinician.

### Key Capabilities

**Core EMR System**
- Patient registration and demographics management
- Visit tracking (chief complaint, exam, assessment, plan, prescriptions, follow-up)
- Medical history with conditions, medications, and allergies
- Vital signs captured per visit (BMI auto-calculated from weight/height)
- Lab tests-ordered text on visits (no structured lab-results entry or trending view yet)
- Immunization records management

**Offline AI Clinical Assistant**
- Local-first - no runtime network calls; all data stays on your machine (unencrypted at rest - see Security note below)
- Completely offline after the one-time model download
- Word-by-word (typewriter) response display (client-side reveal of the full Ollama reply)
- Context-aware clinical Q&A: the LLM sees the patient record; any differential diagnosis or
  interaction check it produces is free text from the model, not a validated rules engine
- Zero cost - no API fees or subscriptions

**Professional Documentation**
- Generate Word reports with clinic letterhead
- Complete patient medical record exports
- One-click document generation

**FHIR Integration**
- Import FHIR R4 Bundle or Patient resources (e.g., Synthea exports)
- Export any patient as a FHIR collection Bundle
- Data validation on import (simplified field mapping, not a FHIR-conformant server)

---

## System Requirements

- **Operating System:** Windows 10+, macOS, or Linux
- **Python:** 3.12 or higher
- **RAM:** 4GB minimum (8GB+ recommended for AI features)
- **Storage:** 500MB + AI model size (0.5-4GB)
- **Internet:** Required only for initial setup and downloads

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/mabdulre9/ai-enabled-healthcare-system.git
cd healthcare-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Open your browser to `http://localhost:5000`

For detailed installation instructions, see [Getting Started](getting-started.html).

---

## Features Overview

### Privacy & Security

- **Local-First Architecture** - All patient data stored locally (SQLite, unencrypted at rest)
- **Offline AI Processing** - No cloud API calls
- **Login Protected** - Shared password gate on all pages and APIs
- **No Third-Party Services** - Your data is not sent to external processors at runtime (the app itself uses open-source libraries: Flask, Werkzeug, python-docx, Pydantic, the ollama client)

*Note: local-only storage reduces exposure but is not "HIPAA compliance." See the
repository README's Security & Compliance Notes for implemented vs. missing safeguards.*

### Cost Effectiveness

- **Open Source** - No licensing fees
- **Free AI** - Ollama models are completely free
- **Zero Subscriptions** - No monthly fees
- **Minimal Infrastructure** - Run on standard hardware

### Technical Excellence

- **FHIR R4 Import/Export** - Exchange patient data as FHIR Bundles (simplified mapping)
- **JSON HTTP API** - REST-style endpoints under `/api/` (no OpenAPI spec / generated reference yet)
- **Clinic-oriented UI** - Simple, functional single-page app (no component framework)
- **Guides** - Getting-started, user-guide, and topic docs below (no full API reference yet)

---

## Use Cases

### Small Clinics

Affordable EMR solution without subscription costs. Complete patient management system with professional documentation and AI assistance.

### Solo Practitioners

Portable system that works offline. Manage patient records, track visits, and get AI-powered clinical insights without connectivity requirements.

### Medical Education

Safe learning environment for clinical documentation. Students can practice with sample patients and receive AI-guided feedback.

### Clinical Research

Structured data collection with FHIR export capabilities. Standardized patient data management for research protocols.

### Remote Healthcare

Reliable operation in areas with limited internet connectivity. Complete EMR functionality without cloud dependencies.

---

## Technical Stack

- **Backend:** Python 3.12+ with Flask 3.0.0
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **AI Engine:** Ollama (local LLM inference)
- **Document Generation:** python-docx
- **Storage:** SQLite (`data/healthcare.db`); each patient/settings record is stored as a JSON blob
- **Standards:** FHIR R4 import/export (simplified mapping)
- **Accessibility:** Semantic HTML with `lang` set; labels are not yet associated with inputs and ARIA attributes are absent, so the UI is **not** WCAG-conformant at any level

---

## Getting Help

- **Installation Guide:** [Getting Started](getting-started.html)
- **User Documentation:** [User Guide](user-guide.html)
- **Common Issues:** [Troubleshooting](troubleshooting.html)
- **GitHub Issues:** [Report a bug](https://github.com/mabdulre9/ai-enabled-healthcare-system/issues)

---

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/mabdulre9/ai-enabled-healthcare-system/blob/main/LICENSE) file for details.

---

## Next Steps

1. [Install the system](getting-started.html) - Complete installation guide
2. [Configure Ollama](installation.html) - Set up offline AI
3. [Learn the basics](user-guide.html) - User guide walkthrough
4. [Explore features](patient-management.html) - Patient management guide
