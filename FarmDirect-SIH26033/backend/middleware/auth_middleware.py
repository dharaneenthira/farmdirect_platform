"""
Authentication & Role-Based Access Control (RBAC) Middleware
"""
from functools import wraps
from flask import request, g, session
from backend.utils.auth import decode_token
from backend.utils.response import error_response
from backend.db.session import db_session
from backend.models.user import User


def require_auth(roles=None):
    """
    Decorator to protect API routes with JWT / Session authentication and RBAC.

    :param roles: String or List of allowed roles (e.g., 'FARMER', ['BUYER', 'ADMIN']).
                  If None, any authenticated user can access the route.
    """
    if isinstance(roles, str):
        roles = [roles.upper()]
    elif isinstance(roles, (list, tuple, set)):
        roles = [r.upper() for r in roles]

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None

            # 1. Look for Bearer Token in Authorization Header
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ", 1)[1]
            elif auth_header:
                token = auth_header.strip()

            # 2. Fallback to session token or user_id
            if not token and "token" in session:
                token = session["token"]

            user = None

            if token:
                try:
                    payload = decode_token(token)
                    user_id = payload.get("user_id")
                    if user_id:
                        user = db_session.get(User, user_id)

                except ValueError as e:
                    return error_response(message=str(e), code=401)
                except Exception as e:
                    return error_response(message="Invalid authentication token", code=401)

            # Fallback to session user_id if token decoding was not used
            if not user and "user_id" in session:
                user = db_session.get(User, session["user_id"])


            if not user:
                return error_response(message="Authentication required. Please log in.", code=401)

            # Role-Based Access Control (RBAC) Check
            if roles and user.role.upper() not in roles:
                return error_response(
                    message=f"Access forbidden: requires one of the following roles: {', '.join(roles)}",
                    code=403,
                )

            # Store authenticated user in Flask request context
            g.current_user = user
            return f(*args, **kwargs)

        return decorated_function

    return decorator
