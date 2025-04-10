from security.connection import PostgreSQLPool
from services.serv_autor_libro import ServAutorLibro
from flask import Blueprint, jsonify, request
from security.auth_token import SecretKeyAuth


serv_autor_libro = ServAutorLibro(PostgreSQLPool())

app_autor_libro = Blueprint("autor_libro", __name__, url_prefix="/autor_libro")


@app_autor_libro.route("/autor_libros/<int:id>", methods=["GET"])
@SecretKeyAuth.token_required
def get_autor_libros(id):
    al = serv_autor_libro.get_autor_libros(id)
    
    libros = [
        {
            "id": l.id,
            "cod": l.cod,
            "titulo": l.titulo,
            "genero": l.genero
        } for l in al.libros
    ]
    
    data = {
        "autor": {
            "id": al.autor.id,
            "cod": al.autor.cod,
            "nombre": al.autor.nombre
        },
        "libros": libros
    }    
    return jsonify(data)


@app_autor_libro.route("/autor_libros/<int:id>", methods=["PUT"])
@SecretKeyAuth.token_required
def update_autor_libros(id):
    message = serv_autor_libro.update_libro_autor(
        id,
        request.json['id_libro'],
        request.json['id_libro_nuevo']
    )
    
    return jsonify({'Mensaje': message})


@app_autor_libro.route("/libro_autores/<int:id>", methods=["GET"])
@SecretKeyAuth.token_required
def get_libro_autores(id):
    la = serv_autor_libro.get_libro_autores(id)
    
    autores = [
        {
            "id": a.id,
            "cod": a.cod,
            "nombre": a.nombre
        } for a in la.autores
    ]
    
    data = {
        "libro": {
            "id": la.libro.id,
            "cod": la.libro.cod,
            "titulo": la.libro.titulo
        },
        "autores": autores
    }
    
    return jsonify(data)


@app_autor_libro.route("/libro_autores/<int:id>", methods=["PUT"])
@SecretKeyAuth.token_required
def update_libro_autores(id):
    message = serv_autor_libro.update_autor_libro(
        id,
        request.json['id_autor'],
        request.json['id_autor_nuevo']
    )
    
    return jsonify({'Mensaje': message})


@app_autor_libro.route("/", methods=["POST"])
@SecretKeyAuth.token_required
def insert_libro_autor():
    message = serv_autor_libro.insert_libro_autor(
        request.json['id_autor'],
        request.json['id_libro']
    )
    
    return jsonify({'Mensaje': message})


@app_autor_libro.route("/", methods=["DELETE"])
@SecretKeyAuth.token_required
def delete_libro_autor():
    message = serv_autor_libro.delete_autor_libro(
        request.json['id_autor'],
        request.json['id_libro']
    )
    
    return jsonify({'Mensaje': message})