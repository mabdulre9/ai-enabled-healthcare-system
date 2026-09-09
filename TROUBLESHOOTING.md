# 🔧 Troubleshooting Guide

## Common Issues & Solutions

This guide helps you fix common problems with the Healthcare EMR System.

---

## 🚀 Installation Issues

### ❌ Error: "Module not found"

**Problem:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Make sure you're in the project directory
cd healthcare-system-v7.1-final

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -i "flask\|ollama\|docx"
```

### ❌ Error: "Python not found"

**Problem:**
```
'python' is not recognized as an internal or external command
```

**Solution:**
1. Install Python 3.12+ from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart terminal
4. Try: `python --version`

---

## 🤖 AI / Ollama Issues

### ❌ Error: "Ollama not installed"

**Problem:**
```
AI Assistant error:
Ollama not installed.
Install: pip install ollama
Download: https://ollama.com/download
```

**Solution:**

**Step 1: Install Ollama Python Package**
```bash
pip install ollama
```

**Step 2: Install Ollama Application**
1. Download from: https://ollama.com/download
2. Install for your OS (Windows/Mac/Linux)
3. Run Ollama (it runs in system tray/background)

**Step 3: Pull a Model**
```bash
ollama pull qwen2.5:4b
```

**Step 4: Verify**
```bash
ollama list
# Should show qwen2.5:4b
```

---

### ❌ Error: "Cannot connect to Ollama"

**Problem:**
```
AI Assistant error:
Cannot connect to Ollama.
Make sure Ollama is running.
```

**Solution:**

**Check 1: Is Ollama Running?**
```bash
# Check if Ollama is running
ollama list

# If not running, start it:
ollama serve
```

**Check 2: Check System Tray (Windows/Mac)**
- Look for Ollama icon in system tray
- If not there, start Ollama application

**Check 3: Check Settings**
1. Go to **⚙️ SETTINGS** in the app
2. Verify "Ollama Host" is: `http://localhost:11434`
3. Click **TEST MODEL**

**Check 4: Firewall**
- Make sure port 11434 is not blocked
- Add exception for Ollama in firewall

---

### ❌ Error: "Model not found"

**Problem:**
```
AI Assistant error:
Model not found: qwen2.5:4b
Download it with: ollama pull qwen2.5:4b
```

**Solution:**

**Step 1: Download the Model**
```bash
ollama pull qwen2.5:4b
```

**Step 2: Verify Download**
```bash
ollama list
# Should show qwen2.5:4b
```

**Step 3: Check Model Name in Settings**
1. Go to **⚙️ SETTINGS**
2. Make sure model name is exactly: `qwen2.5:4b`
3. Click **SAVE SETTINGS**
4. Click **TEST MODEL**

**Alternative Models:**
```bash
# Smaller/faster (2.5GB)
ollama pull qwen2.5:4b

# Larger/better (5GB)
ollama pull qwen2.5:7b

# Even larger (9GB)
ollama pull llama3.1:8b
```

---

### ❌ AI Response is Very Slow

**Problem:**
First query takes 30+ seconds

**This is Normal!**
- **First query**: 15-30 seconds (loading model into RAM)
- **Subsequent queries**: 3-10 seconds

**To Speed Up:**
1. Use smaller model: `qwen2.5:4b` instead of `7b`
2. Close other applications (free up RAM)
3. Keep Ollama running (don't unload model)

---

## 🌐 Server Issues

### ❌ Error: "Port already in use"

**Problem:**
```
OSError: [Errno 98] Address already in use
```

**Solution:**

**Option 1: Use a Different Port**
Set the `FLASK_PORT` environment variable before running (no code edit needed):

```bash
# Windows (cmd)
set FLASK_PORT=5001 && python app.py

# Windows (PowerShell)
$env:FLASK_PORT=5001; python app.py

# Linux/Mac
FLASK_PORT=5001 python app.py
```

Then access at: http://localhost:5001

(The server binds to `127.0.0.1` by default. `FLASK_HOST` overrides the bind address -
keep it localhost-only unless you know why you need otherwise.)

**Option 2: Kill Process Using Port**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

---

### ❌ Error: "Server won't start"

**Problem:**
No output when running `python app.py`

**Solution:**

**Check 1: Right Directory**
```bash
# Make sure you're in the project folder
cd healthcare-system-v7.1-final
ls app.py  # Should exist
```

**Check 2: Python Version**
```bash
python --version
# Should be 3.8 or higher
```

**Check 3: Dependencies**
```bash
pip install -r requirements.txt
```

**Check 4: Check for Errors**
```bash
python -m py_compile app.py
# Should have no output if OK
```

---

## 💾 Data Issues

### ❌ Error: "Patients not saving"

**Problem:**
Created patients disappear after restart

**Solution:**

**Check 1: Data Folder Exists**
```bash
# Create data folder if missing
mkdir data
```

**Check 2: File Permissions**
```bash
# Make sure you can write to data folder
ls -la data/
chmod -R 755 data/  # Linux/Mac
```

**Check 3: Database File**
```bash
# Check if the SQLite database exists
ls -la data/healthcare.db

# If corrupted: restore from your backup copy of data/.
# As a last resort, stop the app and delete healthcare.db -
# WARNING: this loses ALL patients except the two sample records
# that data/patients.json re-seeds on next start.
```

---

### ❌ Settings Not Saving

**Problem:**
Ollama settings reset after restart

**Solution:**

Settings are stored in the `settings` table of `data/healthcare.db` (not a JSON file anymore).

**Check 1: Save Flow**
Use the **⚙️ SETTINGS** page → enter model → click **TEST MODEL** → then **SAVE SETTINGS**.
The page must show a success alert; closing the tab before saving discards edits.

**Check 2: App Writes to Disk**
Confirm the app process can write to `data/` (see "Check 2: File Permissions" above).
Defaults (`qwen2.5:4b`, localhost) are seeded automatically on first run if no settings row exists.

---

## 📄 Document Generation Issues

### ❌ Word Documents Won't Download

**Problem:**
Click "Download Report" but nothing happens

**Solution:**

**Check 1: python-docx Installed**
```bash
pip install python-docx
```

**Check 2: Browser Settings**
- Check browser's download folder
- Allow pop-ups/downloads for localhost

**Check 3: Try Different Browser**
- Chrome, Firefox, Edge, Safari

---

## 🎨 UI Issues

### ❌ Page Looks Broken / Text Not Visible

**Problem:**
Yellow/blue text not visible, layout broken

**This was fixed in v7.1 FINAL!**
- Patient names should be readable
- Patient IDs should be visible
- All text should have good contrast

**If still broken:**
1. Clear browser cache
2. Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
3. Try different browser

---

### ❌ Buttons Not Working

**Problem:**
Clicking buttons does nothing

**Solution:**

**Check 1: JavaScript Enabled**
- Make sure JavaScript is enabled in browser

**Check 2: Browser Console**
1. Press F12
2. Go to "Console" tab
3. Look for errors (red text)
4. Share errors for support

**Check 3: Browser Compatibility**
- Use Chrome, Firefox, Edge, or Safari
- Update browser to latest version

---

## 🔍 Search Issues

### ❌ Search Not Finding Patients

**Problem:**
Patient exists but search returns "No patients found"

**Solution:**

**Search Tips:**
- Search by Patient ID: `PATIENT-001`
- Search by full name: `Robert Johnson`
- Search by first name: `Robert`
- Search by last name: `Johnson`
- Search is case-insensitive

**If still not working:**
1. Check if patient actually exists (scroll patient list)
2. Try exact Patient ID
3. Refresh page

---

## ⚙️ Settings Page Issues

### ❌ Can't Save Settings - "mode not defined" Error

**This was fixed in v7.1 FINAL!**

If you still see this error:
1. You're using old version
2. Download latest v7.1 FINAL
3. Extract and use that

---

### ❌ AI Mode Shows "GEMINI API"

**This was fixed in v7.1 FINAL!**

Should show: **"OLLAMA (OFFLINE)"** in GREEN

If you still see "GEMINI API":
1. You're using old version
2. Download latest v7.1 FINAL
3. Hard refresh browser: Ctrl+F5

---

## 🔒 Privacy & Security

### ❓ Is my patient data safe?

**Private, but "safe" depends on your machine:**
- All data is stored locally in a SQLite database: `data/healthcare.db`
- Never sent to any cloud; the AI runs through local Ollama
- ⚠ The database and downloaded reports are **unencrypted plain files** - anyone with access to the PC (or a stolen laptop) can read them

**Protect it:**
- Keep full-disk encryption ON (Windows BitLocker / macOS FileVault)
- Lock your workstation when away
- Change the default login password (`CLINIC_PASSWORD` env var)
- Don't expose port 5000 beyond localhost (default is `127.0.0.1` - keep it that way)

**Backup Your Data:**
```bash
# Stop the app first, then copy the data folder (includes healthcare.db)
cp -r data/ backup_$(date +%Y%m%d)/
```

---

## 📱 Browser Compatibility

**Tested & Working:**
- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Edge
- ✅ Safari

**May Have Issues:**
- ❌ Internet Explorer (not supported)
- ❌ Very old browsers

---

## 🆘 Getting More Help

### Check Documentation
- `README.md` - Overview and setup
- `QUICKSTART.md` - Quick start guide
- `OLLAMA_GUIDE.md` - Ollama setup details
- `TESTING_CHECKLIST.md` - Test everything

### Check Logs
```bash
# Run app and check output
python app.py

# Look for error messages in terminal
```

### Browser Console
1. Press F12
2. Go to "Console" tab
3. Look for red errors
4. Screenshot and share

---

## ✅ Verification Checklist

Before reporting issues, verify:

- [ ] Python 3.8+ installed: `python --version`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] In correct directory: `ls app.py`
- [ ] Ollama installed (if using AI): `ollama --version`
- [ ] Model downloaded: `ollama list`
- [ ] Ollama running: `ollama list` (no error)
- [ ] Server starts: `python app.py` (no errors)
- [ ] Can access: http://localhost:5000
- [ ] Using v7.1 FINAL (check TESTING_CHECKLIST.md exists)

---

## 🎓 Common Scenarios

### "I just want to use it WITHOUT AI"

**Totally fine!**
1. Skip Ollama installation
2. Just use patient management features
3. Register patients, record visits
4. Generate Word reports
5. Import/export FHIR

The app works perfectly without AI!

---

### "I want to use it offline"

**Works offline!**
- All patient data local
- No internet needed (except initial Ollama download)
- Suitable for air-gapped machines - but see "Is my patient data safe?" above re: encryption

---

### "Can I use this in a clinic?"

**Yes, but...**
- This is a demo/educational system
- NOT certified for production medical use
- Use at your own risk
- Consider proper EMR systems for real clinics

---

**Still having issues? Check the guides in this repository first:**

---

**Last Updated:** March 18, 2026  
**Version:** 7.1 FINAL
