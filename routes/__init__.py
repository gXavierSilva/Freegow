from .user_routes import user_bp
from .role_routes import role_bp
from .patient_routes import patient_bp
from .companie_routes import companie_bp
from .clinic_routes import clinic_bp
from .page_routes import page_bp
from .landing_page_routes import landing_bp

def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(companie_bp)
    app.register_blueprint(clinic_bp)
    app.register_blueprint(page_bp)
    app.register_blueprint(landing_bp)