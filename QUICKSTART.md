# QUICK START GUIDE

## Setup (5 minutes)

### Step 1: Install Python Dependencies
```bash
cd healthcare-system-v7.1-final
pip install -r requirements.txt
```

### Step 2: Install Ollama (Optional - for AI features)
1. Download from: https://ollama.com/download
2. Install and run Ollama
3. Pull a model:
```bash
ollama pull qwen2.5:4b
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Open in Browser
Navigate to: http://localhost:5000

### Step 5: Configure Ollama (if using AI)
1. Click **⚙️ SETTINGS**
2. Enter model name: `qwen2.5:4b`
3. Click **TEST MODEL**
4. Click **SAVE SETTINGS**

## First Steps

1. **Explore Sample Data**: Two patients are pre-loaded
   - Click on "Jane Doe" or "Robert Johnson"
   - Explore their medical records

2. **Register New Patient**: Click "REGISTER NEW PATIENT"
   - Fill in at least: Name, DOB, Gender
   - Add conditions, medications, allergies (optional)
   - Click "SAVE PATIENT RECORD"

3. **Record a Visit**: Select a patient
   - Click "NEW VISIT"
   - Fill in: Date, Type, Chief Complaint, Assessment
   - Add vital signs (optional but recommended)
   - Click "SAVE VISIT RECORD"

4. **Try AI Assistant**: From patient record
   - Click "AI ASSISTANT"
   - Wait for context to load (shows "OLLAMA (OFFLINE)")
   - Ask a question like: "What could be causing increased thirst and frequent urination?"
   - Click "ASK AI ASSISTANT"

## Common Issues

**Problem**: "Port already in use"
**Solution**: Change port in app.py (last line): `port=5001`

**Problem**: "AI not working - Cannot connect to Ollama"
**Solution**: 
- Make sure Ollama is running (check system tray)
- Run: `ollama serve` in terminal
- Check Settings has correct model name

**Problem**: "Model not found"
**Solution**: Download the model: `ollama pull qwen2.5:4b`

**Problem**: "Module not found"
**Solution**: Run `pip install -r requirements.txt`

## Keyboard Shortcuts

- **Search**: Enter in search box, then press Enter
- **AI Assistant**: Press Enter to submit question
- **Forms**: Tab to navigate fields

## Tips

- BMI is auto-calculated when you enter weight and height
- Age is auto-calculated from date of birth
- Patient IDs are auto-generated (PATIENT-001, PATIENT-002, etc.)
- All forms can be saved with incomplete data (only starred fields required)
- Visit history shows newest first
- AI conversation history is kept during session
- All patient data is stored locally in the `data/` folder
- **Privacy**: No cloud APIs - everything runs on your computer

Enjoy using the Healthcare Management System!
