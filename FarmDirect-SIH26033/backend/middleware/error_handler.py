"""
Centralized Flask Error Handlers
"""
from flask import jsonify


def register_error_handlers(app):
    """Registers standard HTTP error handlers with JSON responses"""

    @app.errorhandler(404)
    def handle_not_found(e):
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Resource or endpoint not found",
                    "code": 404,
                }
            ),
            404,
        )

    @app.errorhandler(500)
    def handle_internal_error(e):
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Internal server error",
                    "code": 500,
                }
            ),
            500,
        )

    @app.errorhandler(400)
    def handle_bad_request(e):
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Bad request",
                    "code": 400,
                }
            ),
            400,
        )
