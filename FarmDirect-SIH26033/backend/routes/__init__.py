"""
Routes Package Initialization
"""
from .health_routes import health_bp
from .auth_routes import auth_bp
from .farmer_routes import farmer_bp
from .buyer_routes import buyer_bp
from .admin_routes import admin_bp
from .marketplace_routes import marketplace_bp
from .ai_routes import ai_bp

__all__ = [
    "health_bp",
    "auth_bp",
    "farmer_bp",
    "buyer_bp",
    "admin_bp",
    "marketplace_bp",
    "ai_bp",
]
