from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.auth import login_required
from app.data import load_settings, save_settings
from app.models import Settings

settings_bp = Blueprint('settings', __name__)


def _validation_errors(e):
    return [
        {'loc': [str(x) for x in err.get('loc', [])], 'msg': err.get('msg', ''), 'type': err.get('type', '')}
        for err in e.errors()
    ]


@settings_bp.route('/api/settings', methods=['GET'])
@login_required
def api_get_settings():
    return jsonify(load_settings())


@settings_bp.route('/api/settings', methods=['POST'])
@login_required
def api_save_settings():
    try:
        new_settings = request.json
        validated = Settings(**new_settings)
        save_settings(validated.model_dump())
        return jsonify({'success': True})
    except ValidationError as e:
        return jsonify({'error': 'Validation failed', 'details': _validation_errors(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@settings_bp.route('/api/settings/test-model', methods=['POST'])
@login_required
def api_test_model():
    try:
        settings = request.json
        try:
            import ollama

            model_name = settings.get('ollama_model', 'qwen2.5:4b')

            response = ollama.chat(
                model=model_name,
                messages=[
                    {'role': 'user', 'content': 'Say hello in one sentence.'}
                ],
                options={
                    'num_predict': 50
                }
            )

            return jsonify({
                'message': f'Ollama Test Successful!\n\nModel: {model_name}\nStatus: Running\nResponse: {response["message"]["content"][:100]}'
            })

        except ImportError:
            return jsonify({'error': 'Ollama not installed.\n\nInstall: pip install ollama\nDownload: https://ollama.com/download'}), 500
        except Exception as e:
            error_msg = str(e)
            if 'connect' in error_msg.lower():
                return jsonify({'error': 'Cannot connect to Ollama.\n\nMake sure Ollama is running (check system tray or run: ollama serve)'}), 500
            elif 'not found' in error_msg.lower():
                return jsonify({'error': f'Model not found: {model_name}\n\nDownload it with: ollama pull {model_name}'}), 500
            else:
                return jsonify({'error': f'Ollama error: {error_msg}'}), 500

    except Exception as e:
        return jsonify({'error': f'Test failed: {str(e)}'}), 500


@settings_bp.route('/api/ollama/unload', methods=['POST'])
@login_required
def api_ollama_unload():
    try:
        import ollama
        import subprocess

        result = subprocess.run(['ollama', 'ps'], capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': 'Could not check Ollama status'}), 500

        output = result.stdout
        lines = output.strip().split('\n')

        if len(lines) <= 1:
            return jsonify({'message': 'No models currently loaded in memory'}), 200

        try:
            import platform

            if platform.system() == 'Windows':
                subprocess.run(['powershell', '-Command', 'Stop-Process', '-Name', 'ollama', '-Force'],
                             capture_output=True)
                import time
                time.sleep(1)
                return jsonify({
                    'message': 'Ollama restarted - all models unloaded from memory!\n\nMemory has been freed. Next query will reload the model.'
                }), 200
            else:
                subprocess.run(['pkill', 'ollama'], capture_output=True)
                import time
                time.sleep(1)
                return jsonify({
                    'message': 'Ollama stopped - all models unloaded from memory!\n\nMemory has been freed. Ollama will restart on next query.'
                }), 200

        except Exception as e:
            return jsonify({
                'error': f'Could not unload model: {str(e)}\n\nYou can manually stop Ollama from system tray or task manager.'
            }), 500

    except ImportError:
        return jsonify({'error': 'Ollama not installed'}), 500
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500
