import json
import os
import sqlite3
from app.config import DATA_FILE, SETTINGS_FILE, DATABASE_FILE, OLLAMA_SETTINGS


def get_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA foreign_keys=ON')
    return conn


def init_db():
    os.makedirs('data', exist_ok=True)
    conn = get_connection()
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                data TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                data TEXT NOT NULL
            )
        ''')
        conn.commit()
        _migrate_from_json(conn)
        if not conn.execute('SELECT 1 FROM settings WHERE id = 1').fetchone():
            conn.execute('INSERT INTO settings (id, data) VALUES (1, ?)',
                         (json.dumps(OLLAMA_SETTINGS, ensure_ascii=False),))
            conn.commit()
    finally:
        conn.close()


def _migrate_from_json(conn):
    if not conn.execute('SELECT 1 FROM patients LIMIT 1').fetchone() and os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                patients = json.load(f)
            if isinstance(patients, list) and patients:
                for p in patients:
                    pid = p.get('patientId')
                    if pid:
                        conn.execute('INSERT OR REPLACE INTO patients (patient_id, data) VALUES (?, ?)',
                                     (pid, json.dumps(p, ensure_ascii=False)))
                conn.commit()
            os.rename(DATA_FILE, DATA_FILE + '.bak')
        except Exception:
            pass

    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            if not conn.execute('SELECT 1 FROM settings WHERE id = 1').fetchone():
                conn.execute('INSERT INTO settings (id, data) VALUES (1, ?)',
                             (json.dumps(settings, ensure_ascii=False),))
                conn.commit()
            os.rename(SETTINGS_FILE, SETTINGS_FILE + '.bak')
        except Exception:
            pass


def load_settings():
    conn = get_connection()
    try:
        row = conn.execute('SELECT data FROM settings WHERE id = 1').fetchone()
        if row:
            return json.loads(row['data'])
        return OLLAMA_SETTINGS.copy()
    except Exception:
        return OLLAMA_SETTINGS.copy()
    finally:
        conn.close()


def save_settings(settings):
    conn = get_connection()
    try:
        conn.execute('INSERT OR REPLACE INTO settings (id, data) VALUES (1, ?)',
                     (json.dumps(settings, ensure_ascii=False),))
        conn.commit()
    finally:
        conn.close()


def list_patients():
    conn = get_connection()
    try:
        rows = conn.execute('SELECT data FROM patients ORDER BY rowid').fetchall()
        return [json.loads(r['data']) for r in rows]
    finally:
        conn.close()


def get_patient(patient_id):
    conn = get_connection()
    try:
        row = conn.execute('SELECT data FROM patients WHERE patient_id = ?', (patient_id,)).fetchone()
        return json.loads(row['data']) if row else None
    finally:
        conn.close()


def patient_exists(patient_id):
    conn = get_connection()
    try:
        return conn.execute('SELECT 1 FROM patients WHERE patient_id = ?', (patient_id,)).fetchone() is not None
    finally:
        conn.close()


def upsert_patient(patient):
    conn = get_connection()
    try:
        conn.execute('INSERT OR REPLACE INTO patients (patient_id, data) VALUES (?, ?)',
                     (patient['patientId'], json.dumps(patient, ensure_ascii=False)))
        conn.commit()
    finally:
        conn.close()


def delete_patient(patient_id):
    conn = get_connection()
    try:
        cur = conn.execute('DELETE FROM patients WHERE patient_id = ?', (patient_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def generate_patient_id():
    conn = get_connection()
    try:
        rows = conn.execute('SELECT patient_id FROM patients').fetchall()
    finally:
        conn.close()

    max_id = 0
    for row in rows:
        try:
            num = int(row['patient_id'].split('-')[1])
            if num > max_id:
                max_id = num
        except (IndexError, ValueError):
            continue
    return f'PATIENT-{str(max_id + 1).zfill(3)}'


def generate_visit_id(patient_id):
    patient = get_patient(patient_id)
    if not patient or not patient.get('visits'):
        return f'{patient_id}-VISIT-001'
    max_id = len(patient['visits'])
    return f'{patient_id}-VISIT-{str(max_id + 1).zfill(3)}'
