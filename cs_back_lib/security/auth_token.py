import jwt
from functools import wraps
from flask import request, jsonify

class SecretKeyAuth:
    @staticmethod
    def get_secret_key():
        with open('../sec_workspace/SECRET_KEY.arvl', 'r') as file:
            return file.read().strip()
        
    @staticmethod
    def token_required(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                return jsonify({"Error": "No hay Token o es inválido"}), 400
            try:
                jwt.decode(token.split()[1], SecretKeyAuth.get_secret_key(), algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                return jsonify({"Error": "El Token ha expirado"}), 401
            except jwt.InvalidTokenError:
                return jsonify({"Error": "El Token es inválido"}), 401
            return f(*args, **kwargs)
        return wrapper
