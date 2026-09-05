"""
Admin Command Center Routes
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""
from flask import Blueprint, g, request
from backend.middleware.auth_middleware import require_auth
from backend.utils.response import success_response
from backend.db.session import db_session
from backend.models.user import AdminActivity

admin_bp = Blueprint("admin", __name__)



@admin_bp.route("/metrics", methods=["GET"])
@require_auth(roles=["ADMIN"])
def admin_metrics():
    """
    Protected Admin Metrics Endpoint
    Requires ADMIN role strictly.
    """
    user = g.current_user
    try:
        audit = AdminActivity(
            admin_id=user.id,
            action="VIEW_ADMIN_METRICS",
            ip_address=request.remote_addr,
        )
        db_session.add(audit)
        db_session.commit()
    except Exception:
        db_session.rollback()

    return success_response(
        message="Admin metrics retrieved successfully",
        data={
            "user": user.to_dict(),
            "platform_metrics": {
                "total_users": 0,
                "verified_farmers": 0,
                "verified_buyers": 0,
                "active_anomalies_detected": 0,
            },
        },
        code=200,
    )
