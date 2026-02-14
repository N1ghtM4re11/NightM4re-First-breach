from flask import Flask
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per hour"]
)

def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object("app.config.Config")

    # Initialize security extensions
    csrf.init_app(app)
    limiter.init_app(app)

    # Security headers
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "style-src 'self'; "
            "script-src 'self'; "
            "object-src 'none'"
        )
        return response

    # Register blueprints (later)
    from app.routes import main_bp
    from app.auth import auth_bp
    from app.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Error handlers
    @app.errorhandler(403)
    def forbidden(e):
        return "403 Forbidden", 403

    @app.errorhandler(404)
    def not_found(e):
        return "404 Not Found", 404

    return app
