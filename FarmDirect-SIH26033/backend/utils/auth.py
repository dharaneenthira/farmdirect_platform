"""
JWT Authentication Utility Functions
"""
from datetime import datetime, timedelta, timezone
import jwt
from backend.config import get_config

config = get_config()


def generate_token(user, expires_in_seconds=86400):
    """
    Generates a signed JWT token for an authenticated user.
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "user_id": user.id,
        "phone_number": user.phone_number,
        "role": user.role,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in_seconds),
    }

    secret_key = getattr(config, "JWT_SECRET_KEY", config.SECRET_KEY)
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def decode_token(token):
    """
    Decodes and validates a JWT token.
    Returns the decoded payload dict or raises ValueError on error.
    """
    if not token:
        raise ValueError("Token is required")

    # Strip 'Bearer ' prefix if passed directly
    if token.startswith("Bearer ") or token.startswith("bearer "):
        token = token.split(" ", 1)[1]

    secret_key = getattr(config, "JWT_SECRET_KEY", config.SECRET_KEY)

    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Authentication token has expired")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid authentication token: {str(e)}")
