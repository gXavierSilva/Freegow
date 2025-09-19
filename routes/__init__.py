from .user_routes import user_bp
from .page_routes import page_bp
from .landing_page_routes import landing_bp
from .role_routes import role_bp

def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(page_bp)
    app.register_blueprint(landing_bp)
    app.register_blueprint(role_bp)