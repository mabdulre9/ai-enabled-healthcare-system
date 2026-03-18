---
layout: default
title: Installation
---

# Installation Guide

Complete installation and setup instructions for the Healthcare Management System.

## System Requirements

- Python 3.12+
- 4GB RAM minimum (8GB+ for AI)
- 500MB storage + AI model size
- Windows 10+, macOS, or Linux

## Python Installation

Install Python from [python.org/downloads](https://www.python.org/downloads/)

Verify installation:
```bash
python --version
```

## Application Setup

### Clone Repository

```bash
git clone https://github.com/mabdulre9/healthcare-system.git
cd healthcare-system
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

Access at `http://localhost:5000`

## Ollama Installation

### Download Ollama

Visit [ollama.com/download](https://ollama.com/download)

- Windows: Run OllamaSetup.exe
- macOS: Install from DMG
- Linux: `curl -fsSL https://ollama.com/install.sh | sh`

### Download Model

```bash
ollama pull qwen2.5:4b
```

### Configure

1. Open `http://localhost:5000/settings`
2. Enter model name: `qwen2.5:4b`
3. Click TEST MODEL
4. Click SAVE SETTINGS

## Verification

Test all components:

1. Application runs without errors
2. Dashboard displays sample patients
3. AI Assistant connects to Ollama
4. Medical reports generate successfully

## Next Steps

- [Getting Started](getting-started.html)
- [User Guide](user-guide.html)
- [Configuration](configuration.html)
