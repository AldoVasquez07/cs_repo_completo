from security.connection import PostgreSQLPool
from services.serv_libro_genero import ServLibroGenero
from flask import Blueprint, jsonify, request
from security.auth_token import SecretKeyAuth


serv_libro_genero = ServLibroGenero(PostgreSQLPool())

app_libro_genero = Blueprint("libro_genero", __name__, url_prefix="/libro_genero")


@app_libro_genero.route("/libro_generos/<int:id>", methods=["GET"])
@SecretKeyAuth.token_required
def get_libro_generos(id):
    lg = serv_libro_genero.get_libro_generos(id)
    
    generos = [
        {
            "id": g.id,
            "nombre": g.nombre
        } for g in lg.generos
    ]
    
    data = {
        "libro": {
            "id": lg.libro.id,
            "cod": lg.libro.cod,
            "titulo": lg.libro.titulo
        },
        "generos": generos
    }
    
    return jsonify(data)


@app_libro_genero.route("/libro_generos/<int:id>", methods=["PUT"])
@SecretKeyAuth.token_required
def update_libro_generos(id):
    message = serv_libro_genero.update_libro_genero(
        id,
        request.json['id_genero'],
        request.json['id_genero_nuevo']
    )
    
    return jsonify({'Mensaje': message})


@app_libro_genero.route("/genero_libros/<int:id>", methods=["GET"])
@SecretKeyAuth.token_required
def get_genero_libros(id):
    lg = serv_libro_genero.get_genero_libros(id)
    
    libros = [
        {
            "id": l.id,
            "cod": l.cod,
            "titulo": l.titulo
        } for l in lg.libros
    ]
    
    data = {
        "genero": {
            "id": lg.genero.id,
            "nombre": lg.genero.nombre
        },
        "libros": libros
    }
    
    return jsonify(data)


@app_libro_genero.route("/genero_libros/<int:id>", methods=["PUT"])
@SecretKeyAuth.token_required
def update_genero_libros(id):
    message = serv_libro_genero.update_genero_libro(
        id,
        request.json['id_libro'],
        request.json['id_libro_nuevo']
    )
    
    return jsonify({'Mensaje': message})


@app_libro_genero.route("/", methods=["POST"])
@SecretKeyAuth.token_required
def insert_libro_genero():
    message = serv_libro_genero.insert_libro_genero(
        request.json['id_libro'],
        request.json['id_genero']
    )
    
    return jsonify({'Mensaje': message})


@app_libro_genero.route("/", methods=["DELETE"])
@SecretKeyAuth.token_required
def delete_libro_genero():
    message = serv_libro_genero.delete_libro_genero(
        request.json['id_libro'],
        request.json['id_genero']
    )
    
    return jsonify({'Mensaje': message})