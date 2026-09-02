"""
Standardized REST API Response Utilities
"""
from flask import jsonify


def api_response(status="success", message="", data=None, code=200):
    """Generates standard JSON API response structure"""
    payload = {
        "status": status,
        "message": message,
    }
    if data is not None:
        payload["data"] = data
    return jsonify(payload), code


def success_response(message="Success", data=None, code=200):
    return api_response(status="success", message=message, data=data, code=code)


def error_response(message="Error", code=400, data=None):
    return api_response(status="error", message=message, data=data, code=code)
