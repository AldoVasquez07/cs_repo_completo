from functools import wraps
import jwt
from security.secret_key import SecretKeyAuth
from flask import request, jsonify

SECRET_KEY = SecretKeyAuth.get_secret_key()


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"Error": "No hay Token o es inválido"}), 400
        try:
            jwt.decode(token.split()[1], SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"Error": "El Token ha expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"Error": "El Token es inválido"}), 401
        return f(*args, **kwargs)
    return wrapper
    