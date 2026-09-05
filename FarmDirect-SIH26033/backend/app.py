"""
FarmDirect Backend Application Entrypoint
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""
import os
import sys

# Ensure backend package can be resolved when app.py is executed directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask
from flask_cors import CORS
from backend.config import get_config
from backend.db.session import init_db, db_session
from backend.middleware.error_handler import register_error_handlers
from backend.routes import (
    health_bp,
    auth_bp,
    farmer_bp,
    buyer_bp,
    admin_bp,
    marketplace_bp,
    ai_bp,
)


def create_app(config_class=None):
    """
    Application Factory Pattern for Flask Server Initialization
    """
    app = Flask(__name__)

    if config_class is None:
        config_class = get_config()

    app.config.from_object(config_class)

    # Rebind DB engine/session if specific URI is configured (e.g. testing)
    uri = app.config.get("SQLALCHEMY_DATABASE_URI")
    if uri:
        init_db(uri=uri, create_tables=False)

    # Cleanup SQLAlchemy scoped session on context teardown
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # Configure CORS for local frontend development
    CORS(
        app,
        resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}},
        supports_credentials=True,
    )

    # Register Modular Blueprints
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(farmer_bp, url_prefix="/api/farmer")
    app.register_blueprint(buyer_bp, url_prefix="/api/buyer")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(marketplace_bp, url_prefix="/api/marketplace")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")


    # Register Centralized Error Handlers
    register_error_handlers(app)

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    # Create tables when running app server directly
    with app.app_context():
        try:
            init_db(create_tables=True)
        except Exception as err:
            app.logger.warning(f"Database initialization warning: {err}")
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])
