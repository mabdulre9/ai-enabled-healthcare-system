from functools import wraps
from flask import session, redirect, url_for, request, jsonify
from app.config import CLINIC_PASSWORD


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('authenticated'):
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Authentication required'}), 401
            return redirect(url_for('pages.login'))
        return f(*args, **kwargs)
    return decorated


def verify_password(password):
    return password == CLINIC_PASSWORD
