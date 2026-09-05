"""
Buyer Routes
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""
from flask import Blueprint, g
from backend.middleware.auth_middleware import require_auth
from backend.utils.response import success_response

buyer_bp = Blueprint("buyer", __name__)



@buyer_bp.route("/dashboard", methods=["GET"])
@require_auth(roles=["BUYER", "ADMIN"])
def buyer_dashboard():
    """
    Protected Buyer Dashboard Endpoint
    Requires BUYER or ADMIN role.
    """
    user = g.current_user
    return success_response(
        message=f"Welcome to Buyer Dashboard, {user.full_name}",
        data={
            "user": user.to_dict(),
            "summary": {
                "active_orders": 0,
                "total_purchases_inr": 0.0,
                "saved_listings": 0,
            },
        },
        code=200,
    )
