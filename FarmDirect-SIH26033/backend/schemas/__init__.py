"""
Validation Schemas Package
"""
from .auth_schema import validate_registration_data, validate_login_data

__all__ = ["validate_registration_data", "validate_login_data"]

