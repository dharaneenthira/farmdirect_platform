"""
Farmer Routes
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""
from flask import Blueprint, g
from backend.middleware.auth_middleware import require_auth
from backend.utils.response import success_response

farmer_bp = Blueprint("farmer", __name__)



@farmer_bp.route("/dashboard", methods=["GET"])
@require_auth(roles=["FARMER", "ADMIN"])
def farmer_dashboard():
    """
    Protected Farmer Dashboard Endpoint
    Requires FARMER or ADMIN role.
    """
    user = g.current_user
    return success_response(
        message=f"Welcome to Farmer Dashboard, {user.full_name}",
        data={
            "user": user.to_dict(),
            "summary": {
                "active_listings": 0,
                "total_sales_inr": 0.0,
                "pending_bids": 0,
            },
        },
        code=200,
    )
