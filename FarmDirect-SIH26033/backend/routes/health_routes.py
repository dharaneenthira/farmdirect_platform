"""
Health Check Blueprint
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""
from flask import Blueprint, jsonify
from backend.db.session import check_db_connection

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """
    GET /api/health
    Returns backend operational status and database connection status.
    """
    db_connected = check_db_connection()
    db_status = "connected" if db_connected else "disconnected"

    return jsonify({
        "status": "success",
        "backend": "running",
        "database": db_status
    }), 200
