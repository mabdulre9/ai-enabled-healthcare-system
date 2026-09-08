def register_routes(app):
    from app.routes.pages import pages_bp
    from app.routes.patients import patients_bp
    from app.routes.visits import visits_bp
    from app.routes.ai import ai_bp
    from app.routes.settings import settings_bp
    from app.routes.reports import reports_bp

    app.register_blueprint(pages_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(visits_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(reports_bp)
