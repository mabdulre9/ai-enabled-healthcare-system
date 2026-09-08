from flask import Blueprint, request, jsonify
from app.auth import login_required
from app.data import get_patient, load_settings
from app.services.ai_service import build_patient_context

ai_bp = Blueprint('ai', __name__)


@ai_bp.route('/api/ai-query', methods=['POST'])
@login_required
def api_ai_query():
    data = request.json
    patient_id = data.get('patientId')
    question = data.get('question')

    if not patient_id or not question:
        return jsonify({'error': 'Missing patientId or question'}), 400

    patient = get_patient(patient_id)

    if not patient:
        return jsonify({'error': 'Patient not found'}), 404

    context = build_patient_context(patient)
    settings = load_settings()

    try:
        import ollama

        system_prompt = settings.get('system_prompt', 'You are a clinical AI assistant.')
        full_prompt = f"{context}\n\nDoctor's Question: {question}"

        response = ollama.chat(
            model=settings.get('ollama_model', 'qwen2.5:4b'),
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': full_prompt}
            ],
            options={
                'temperature': settings.get('temperature', 0.7),
                'num_predict': settings.get('max_tokens', 2048)
            }
        )

        return jsonify({
            'response': response['message']['content'],
            'source': 'ollama'
        })

    except ImportError:
        return jsonify({'error': 'Ollama not installed.\n\nInstall: pip install ollama\nDownload: https://ollama.com/download'}), 500
    except Exception as e:
        error_msg = str(e)
        if 'connect' in error_msg.lower():
            return jsonify({'error': 'Cannot connect to Ollama.\n\nMake sure Ollama is running.'}), 500
        elif 'not found' in error_msg.lower():
            model = settings.get('ollama_model', 'qwen2.5:4b')
            return jsonify({'error': f'Model not found: {model}\n\nDownload: ollama pull {model}'}), 500
        else:
            return jsonify({'error': f'Ollama error: {error_msg}'}), 500
