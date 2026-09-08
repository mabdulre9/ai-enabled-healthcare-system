import os
from flask import Flask
from app.data import init_db
from app.routes import register_routes

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app():
    init_db()

    app = Flask(
        __name__,
        template_folder=os.path.join(PROJECT_ROOT, 'templates'),
        static_folder=os.path.join(PROJECT_ROOT, 'static')
    )
    app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

    register_routes(app)

    return app
