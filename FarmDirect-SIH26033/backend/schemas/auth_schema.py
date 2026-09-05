"""
Authentication Request Input Validation Schemas
"""
import re
from backend.models.user import VALID_ROLES


def validate_phone_number(phone):
    """Validates phone number format (10-15 digits, optional + prefix)"""
    if not phone or not isinstance(phone, str):
        return False
    cleaned = phone.strip()
    pattern = r"^\+?[0-9]{10,15}$"
    return bool(re.match(pattern, cleaned))


def validate_email(email):
    """Validates basic email string format"""
    if not email or not isinstance(email, str):
        return False
    cleaned = email.strip()
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, cleaned))


def validate_registration_data(data):
    """
    Validates user registration payload.
    Returns: (is_valid: bool, result: dict)
    """
    if not isinstance(data, dict):
        return False, {"message": "Invalid payload format. Expected JSON object."}

    errors = {}

    # 1. Full Name
    full_name = data.get("full_name")
    if not full_name or not isinstance(full_name, str) or not full_name.strip():
        errors["full_name"] = "Full name is required"
    elif len(full_name.strip()) < 2:
        errors["full_name"] = "Full name must be at least 2 characters long"

    # 2. Phone Number
    phone_number = data.get("phone_number")
    if not phone_number:
        errors["phone_number"] = "Phone number is required"
    elif not validate_phone_number(str(phone_number)):
        errors["phone_number"] = "Invalid phone number format (10-15 digits required)"

    # 3. Password
    password = data.get("password")
    if not password or not isinstance(password, str):
        errors["password"] = "Password is required"
    elif len(password) < 6:
        errors["password"] = "Password must be at least 6 characters long"

    # 4. Role
    role = data.get("role")
    if not role or not isinstance(role, str):
        errors["role"] = f"Role is required. Must be one of: {', '.join(VALID_ROLES)}"
    elif role.upper() not in VALID_ROLES:
        errors["role"] = f"Invalid role '{role}'. Allowed roles: {', '.join(VALID_ROLES)}"

    # 5. Email (Optional)
    email = data.get("email")
    if email and not validate_email(str(email)):
        errors["email"] = "Invalid email format"

    if errors:
        return False, {"message": "Validation failed", "errors": errors}

    cleaned_data = {
        "full_name": full_name.strip(),
        "phone_number": str(phone_number).strip(),
        "password": password,
        "role": role.upper(),
        "email": email.strip() if email else None,
        "profile": data.get("profile", {}) or {},
    }

    # Extract top-level profile fields if present
    if cleaned_data["role"] == "FARMER":
        cleaned_data["profile"].setdefault("location", data.get("location"))
        cleaned_data["profile"].setdefault("farm_size_acres", data.get("farm_size_acres"))
        cleaned_data["profile"].setdefault("primary_crops", data.get("primary_crops"))
    elif cleaned_data["role"] == "BUYER":
        cleaned_data["profile"].setdefault("business_name", data.get("business_name"))
        cleaned_data["profile"].setdefault("business_type", data.get("business_type"))
        cleaned_data["profile"].setdefault("location", data.get("location"))

    return True, cleaned_data


def validate_login_data(data):
    """
    Validates user login payload.
    Accepts phone_number, email, or identifier (phone or email) + password.
    Returns: (is_valid: bool, result: dict)
    """
    if not isinstance(data, dict):
        return False, {"message": "Invalid payload format. Expected JSON object."}

    errors = {}

    identifier = data.get("identifier") or data.get("phone_number") or data.get("email")
    if not identifier or not isinstance(identifier, str) or not identifier.strip():
        errors["identifier"] = "Phone number or email is required"

    password = data.get("password")
    if not password or not isinstance(password, str):
        errors["password"] = "Password is required"

    role = data.get("role")
    if role and role.upper() not in VALID_ROLES:
        errors["role"] = f"Invalid role '{role}'. Allowed roles: {', '.join(VALID_ROLES)}"

    if errors:
        return False, {"message": "Validation failed", "errors": errors}

    return True, {
        "identifier": identifier.strip(),
        "password": password,
        "role": role.upper() if role else None,
    }
