from flask import Blueprint, render_template, redirect, url_for, request, session
from app.auth import login_required, verify_password

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('authenticated'):
        return redirect(url_for('pages.index'))
    if request.method == 'POST':
        if verify_password(request.form.get('password', '')):
            session['authenticated'] = True
            return redirect(url_for('pages.index'))
        return render_template('login.html', error='Invalid password')
    return render_template('login.html')


@pages_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('pages.login'))


@pages_bp.route('/')
@login_required
def index():
    return render_template('index.html')


@pages_bp.route('/new-patient')
@login_required
def new_patient():
    return render_template('new-patient.html')


@pages_bp.route('/patient-view')
@login_required
def patient_view():
    return render_template('patient-view.html')


@pages_bp.route('/new-visit')
@login_required
def new_visit():
    return render_template('new-visit.html')


@pages_bp.route('/ai-assistant')
@login_required
def ai_assistant():
    return render_template('ai-assistant.html')


@pages_bp.route('/settings')
@login_required
def settings():
    return render_template('settings.html')
