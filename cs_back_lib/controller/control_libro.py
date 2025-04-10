from security.connection import PostgreSQLPool
from services.serv_libro import ServLibro
from flask import Blueprint, jsonify, request
from security.auth_token import SecretKeyAuth


serv_libro = ServLibro(PostgreSQLPool())

app_libro = Blueprint("libro", __name__, url_prefix="/libro")

@app_libro.route("/", methods=["GET"])
@SecretKeyAuth.token_required
def get_libros():
    libros = serv_libro.get_libros()
    data = [{'id':l.id, 'cod':l.cod, 'titulo':l.titulo, 'genero':l.genero} for l in libros]
    return jsonify(data)


@app_libro.route("/<int:id>", methods=["GET"])
@SecretKeyAuth.token_required
def get_libro(id):
    libro = serv_libro.get_libro(id)
    
    if not libro:
        return jsonify({'Error': 'No existe el registro'})
        
    data = {'id':libro.id, 'cod':libro.cod, 'titulo':libro.titulo, 'genero':libro.genero}
    return jsonify(data)


@app_libro.route("/", methods=["POST"])
@SecretKeyAuth.token_required
def crear_libro():
    message = serv_libro.insert_libro(
        request.json['cod'],
        request.json['titulo'],
        request.json['id_genero']
    )
    return jsonify({'Mensaje': message})


@app_libro.route("/<int:id>", methods=["PUT"])
@SecretKeyAuth.token_required
def actualizar_libro(id):
    message = serv_libro.update_libro(
        id,
        request.json['cod'],
        request.json['titulo'],
        request.json['id_genero'],
        request.json['flag']
    )
    return jsonify({'Mensaje': message})


@app_libro.route("/<int:id>", methods=["DELETE"])
@SecretKeyAuth.token_required
def eliminar_libro(id):
    message = serv_libro.delete_libro(id)
    return jsonify({'Mensaje': message})