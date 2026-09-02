"""
Health Check Blueprint
"""
from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """
    GET /api/health
    Returns server operational status.
    """
    return jsonify({
        "status": "success",
        "message": "FarmDirect backend is running"
    }), 200
