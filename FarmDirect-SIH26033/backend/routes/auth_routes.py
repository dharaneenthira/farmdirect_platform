"""
Authentication API Routes
Problem Statement ID: SIH26033 | Team: Shadow Stack
"""
from flask import Blueprint, request, session, g
from sqlalchemy import or_
from backend.db.session import db_session
from backend.models.user import User, FarmerProfile, BuyerProfile, AdminActivity, ROLE_FARMER, ROLE_BUYER, ROLE_ADMIN

from backend.schemas.auth_schema import validate_registration_data, validate_login_data
from backend.utils.auth import generate_token
from backend.utils.response import success_response, error_response
from backend.middleware.auth_middleware import require_auth

auth_bp = Blueprint("auth", __name__)



@auth_bp.route("/register", methods=["POST"])
def register():
    """
    User Registration Endpoint
    Supports Farmer, Buyer, and Admin account creation.
    """
    payload = request.get_json(silent=True) or {}
    is_valid, validation_result = validate_registration_data(payload)

    if not is_valid:
        return error_response(
            message=validation_result.get("message", "Validation failed"),
            code=400,
            data=validation_result.get("errors"),
        )

    data = validation_result
    phone_number = data["phone_number"]
    email = data["email"]
    role = data["role"]

    # Check for existing user with duplicate phone number or email
    existing_user = db_session.query(User).filter(
        or_(
            User.phone_number == phone_number,
            (User.email == email) & (User.email.isnot(None)) & (User.email != "")
        )
    ).first()

    if existing_user:
        if existing_user.phone_number == phone_number:
            return error_response(message="User with this phone number already exists", code=400)
        if email and existing_user.email == email:
            return error_response(message="User with this email already exists", code=400)

    # Create new User model instance
    user = User(
        full_name=data["full_name"],
        phone_number=phone_number,
        email=email,
        role=role,
        is_verified=False,
    )
    user.set_password(data["password"])

    # Attach role-specific profile entity
    profile_data = data.get("profile", {})
    if role == ROLE_FARMER:
        user.farmer_profile = FarmerProfile(
            location=profile_data.get("location"),
            farm_size_acres=float(profile_data.get("farm_size_acres")) if profile_data.get("farm_size_acres") is not None else None,
            primary_crops=profile_data.get("primary_crops"),
        )
    elif role == ROLE_BUYER:
        user.buyer_profile = BuyerProfile(
            business_name=profile_data.get("business_name"),
            business_type=profile_data.get("business_type"),
            location=profile_data.get("location"),
        )

    try:
        db_session.add(user)
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        return error_response(message="Failed to register user due to database error", code=500)

    # Generate JWT authentication token
    token = generate_token(user)

    # Store session for stateful fallback
    session["user_id"] = user.id
    session["token"] = token

    return success_response(
        message=f"{role.capitalize()} registered successfully",
        data={
            "token": token,
            "user": user.to_dict(),
        },
        code=201,
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    User Login Endpoint
    Authenticates Farmer, Buyer, or Admin by phone number / email and password.
    """
    payload = request.get_json(silent=True) or {}
    is_valid, validation_result = validate_login_data(payload)

    if not is_valid:
        return error_response(
            message=validation_result.get("message", "Validation failed"),
            code=400,
            data=validation_result.get("errors"),
        )

    identifier = validation_result["identifier"]
    password = validation_result["password"]
    requested_role = validation_result.get("role")

    # Find user by phone number or email
    user = db_session.query(User).filter(
        or_(
            User.phone_number == identifier,
            User.email == identifier
        )
    ).first()

    if not user or not user.check_password(password):
        return error_response(message="Invalid phone number/email or password", code=401)

    # If role was explicitly specified in request, ensure match
    if requested_role and user.role.upper() != requested_role.upper():
        return error_response(
            message=f"Account exists but is registered as {user.role}, not {requested_role}",
            code=401,
        )

    # Generate JWT token
    token = generate_token(user)

    session["user_id"] = user.id
    session["token"] = token

    # Audit Log Integration for Admin users
    if user.role == ROLE_ADMIN:
        try:
            audit = AdminActivity(
                admin_id=user.id,
                action="ADMIN_LOGIN",
                ip_address=request.remote_addr,
            )
            db_session.add(audit)
            db_session.commit()
        except Exception:
            db_session.rollback()


    return success_response(
        message="Login successful",
        data={
            "token": token,
            "user": user.to_dict(),
        },
        code=200,
    )


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    User Logout Endpoint
    Clears local session data.
    """
    session.clear()
    return success_response(message="Logout successful", code=200)


@auth_bp.route("/profile", methods=["GET"])
@auth_bp.route("/me", methods=["GET"])
@require_auth()
def get_profile():
    """
    Get Current Authenticated User Profile
    """
    return success_response(
        message="User profile retrieved successfully",
        data={"user": g.current_user.to_dict()},
        code=200,
    )


@auth_bp.route("/profile", methods=["PUT"])
@require_auth()
def update_profile():
    """
    Update Authenticated User Profile
    """
    user = g.current_user
    payload = request.get_json(silent=True) or {}

    if "full_name" in payload and payload["full_name"]:
        user.full_name = str(payload["full_name"]).strip()

    if "email" in payload:
        new_email = str(payload["email"]).strip() if payload["email"] else None
        if new_email and new_email != user.email:
            existing = db_session.query(User).filter(User.email == new_email).first()
            if existing:
                return error_response(message="Email is already in use", code=400)
            user.email = new_email

    # Role-specific profile updates
    if user.role == ROLE_FARMER:
        if not user.farmer_profile:
            user.farmer_profile = FarmerProfile(user_id=user.id)
        if "location" in payload:
            user.farmer_profile.location = payload["location"]
        if "farm_size_acres" in payload:
            user.farmer_profile.farm_size_acres = float(payload["farm_size_acres"]) if payload["farm_size_acres"] is not None else None
        if "primary_crops" in payload:
            user.farmer_profile.primary_crops = payload["primary_crops"]

    elif user.role == ROLE_BUYER:
        if not user.buyer_profile:
            user.buyer_profile = BuyerProfile(user_id=user.id)
        if "business_name" in payload:
            user.buyer_profile.business_name = payload["business_name"]
        if "business_type" in payload:
            user.buyer_profile.business_type = payload["business_type"]
        if "location" in payload:
            user.buyer_profile.location = payload["location"]

    try:
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        return error_response(message="Failed to update profile", code=500)

    return success_response(
        message="Profile updated successfully",
        data={"user": user.to_dict()},
        code=200,
    )
