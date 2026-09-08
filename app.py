import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', '5000'))

    print("\n" + "=" * 50)
    print("Healthcare Management System")
    print("=" * 50)
    print(f"\nStarting server...")
    print(f"Access: http://localhost:{port}")
    print(f"Debug: {'ON' if debug else 'OFF'}")
    print(f"\nPress Ctrl+C to stop the server\n")

    app.run(debug=debug, host=host, port=port)
