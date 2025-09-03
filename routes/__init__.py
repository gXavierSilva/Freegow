from .user_routes import user_bp
from .page_routes import page_bp

def register_routes(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(page_bp)