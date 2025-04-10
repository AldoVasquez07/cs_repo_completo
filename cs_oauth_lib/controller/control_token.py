from security.connection import PostgreSQLPool
from services.serv_usuario import ServUsuario
from flask import Blueprint, jsonify, request
from security.secret_key import SecretKeyAuth
import jwt
import datetime
import uuid
import secrets


SECRET_KEY = SecretKeyAuth.get_secret_key()
serv_usuario = ServUsuario(PostgreSQLPool())

app_token = Blueprint("token", __name__, url_prefix="/token")


@app_token.route('/', methods=['POST'])
def generate_token():
    auth = request.authorization
    if not serv_usuario.get_usuario(auth.username, auth.password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = jwt.encode({
        'user': auth.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'jti': str(uuid.uuid4())
    }, SECRET_KEY, algorithm='HS256')
    
    return jsonify({'token': token})
