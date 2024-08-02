# decorators.py
from functools import wraps
from flask import request, jsonify, session

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get('rol_id')
            if user_role not in allowed_roles:
                return jsonify({"message": "Unauthorized"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
