---
layout: default
title: Getting Started
---

# Getting Started

This guide will walk you through installing and configuring the Healthcare Management System.

## Prerequisites

Before beginning installation, ensure you have:

- **Python 3.12 or higher** - [Download Python](https://www.python.org/downloads/)
- **Git** (optional) - For cloning the repository
- **Ollama** (optional) - For offline AI features

## Installation Steps

### Step 1: Obtain the Source Code

**Option A: Clone with Git**

```bash
git clone https://github.com/mabdulre9/healthcare-system.git
cd healthcare-system
```

**Option B: Download ZIP**

1. Visit the [GitHub repository](https://github.com/mabdulre9/healthcare-system)
2. Click "Code" → "Download ZIP"
3. Extract the archive
4. Navigate to the extracted directory

### Step 2: Create Virtual Environment

Create an isolated Python environment for the application:

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

### Step 3: Install Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

This installs:
- Flask 3.0.0 - Web framework
- python-docx 1.1.0 - Document generation
- requests 2.31.0 - HTTP library
- ollama - AI integration

### Step 4: Run the Application

Start the development server:

```bash
python app.py
```

Expected output:
```
* Running on http://127.0.0.1:5000
* Press CTRL+C to quit
```

### Step 5: Access the Application

Open your web browser and navigate to:

```
http://localhost:5000
```

You should see the dashboard with two sample patients pre-loaded.

## Ollama AI Setup

To enable the offline AI assistant, install and configure Ollama.

### Install Ollama

Visit [https://ollama.com/download](https://ollama.com/download)

**Windows:**
1. Download `OllamaSetup.exe`
2. Run the installer
3. Ollama starts automatically

**macOS:**
1. Download the DMG file
2. Drag Ollama to Applications
3. Launch Ollama

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Verify Installation:**
```bash
ollama --version
```

### Download AI Model

Select and download an AI model:

**Recommended (Balanced):**
```bash
ollama pull qwen2.5:4b
```

**Fast (Low Resource):**
```bash
ollama pull qwen3:0.6b
```

**High Quality:**
```bash
ollama pull llama3.2:3b
```

**Verify Download:**
```bash
ollama list
```

### Configure AI in Application

1. Navigate to `http://localhost:5000/settings`
2. Enter the model name (e.g., `qwen2.5:4b`)
3. Click **TEST MODEL** to verify connection
4. Click **SAVE SETTINGS**

The AI Assistant is now ready for use.

## First Steps

### Explore Sample Data

The system includes two sample patients:
- Jane Doe - Diabetic patient with visit history
- Robert Johnson - Hypertensive patient

Click on either patient to explore:
- Patient overview and demographics
- Medical history
- Visit records
- Vital signs
- Lab results
- Immunizations

### Register a New Patient

1. Click **REGISTER NEW PATIENT** on the dashboard
2. Complete required fields:
   - Full Name
   - Date of Birth
   - Gender
3. Optionally add:
   - Contact information
   - Medical conditions
   - Current medications
   - Known allergies
4. Click **SAVE PATIENT RECORD**

### Record a Visit

1. Select a patient from the dashboard
2. Click **NEW VISIT**
3. Enter visit information:
   - Visit date (defaults to today)
   - Visit type (Consultation, Follow-up, Emergency)
   - Chief complaint
   - Assessment and plan
4. Optionally record vital signs
5. Click **SAVE VISIT RECORD**

### Use AI Assistant

1. From a patient record, click **AI ASSISTANT**
2. Wait for patient context to load
3. Enter a clinical question
4. Click **ASK AI ASSISTANT** or press Enter
5. View the streaming response

## Configuration

### Clinic Information

Edit clinic details in `app.py` (lines 18-22):

```python
CLINIC_NAME = 'Your Clinic Name'
CLINIC_ADDRESS = '123 Medical Center Dr'
CLINIC_PHONE = '(555) 123-4567'
CLINIC_EMAIL = 'contact@clinic.com'
```

These details appear on generated medical reports.

### Change Application Port

If port 5000 is in use, modify `app.py` (last line):

```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change port
```

## Troubleshooting

### Port Already in Use

**Error:** "Address already in use"

**Solution:** Change the port in `app.py` as described above.

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:** Ensure virtual environment is activated and run:
```bash
pip install -r requirements.txt
```

### Ollama Connection Failed

**Error:** Cannot connect to Ollama

**Solution:**
1. Verify Ollama is running: `ollama list`
2. Ensure model is downloaded: `ollama pull qwen2.5:4b`
3. Test model in Settings page
4. Restart Ollama service if necessary

### Python Version Error

**Error:** Python version too old

**Solution:** Install Python 3.12+ from [python.org](https://www.python.org/downloads/)

## Next Steps

- [User Guide](user-guide.html) - Learn core features
- [Patient Management](patient-management.html) - Manage patient records
- [AI Assistant](ai-assistant.html) - Use AI clinical support
- [Configuration](configuration.html) - Advanced settings
