from security.connection import PostgreSQLPool
from services.serv_autor import ServAutor
from flask import Blueprint, jsonify, request
from security.token import token_required


serv_autor = ServAutor(PostgreSQLPool())

app_autor = Blueprint("autor", __name__, url_prefix="/autor")


@app_autor.route("/", methods=["GET"])
@token_required
def get_autores():
    autores = serv_autor.get_autores()
    data = [{'id':a.id, 'cod':a.cod, 'nombre':a.nombre} for a in autores]
    return jsonify(data)


@app_autor.route("/<int:id>", methods=["GET"])
@token_required
def get_autor(id):
    autor = serv_autor.get_autor(id)
    
    if not autor:
        return jsonify({'Error': 'No existe el registro'})
        
    data = {'id':autor.id, 'cod':autor.cod, 'nombre':autor.nombre}
    return jsonify(data)


@app_autor.route("/", methods=["POST"])
@token_required
def crear_autor():
    message = serv_autor.insert_autor(
        request.json['cod'],
        request.json['nombre'],
        request.json['apellido_paterno'],
        request.json['apellido_materno']
    )
    return jsonify({'Mensaje': message})


@app_autor.route("/<int:id>", methods=["PUT"])
@token_required
def actualizar_autor(id):
    message = serv_autor.update_autor(
        id,
        request.json['cod'],
        request.json['nombre'],
        request.json['apellido_paterno'],
        request.json['apellido_materno'],
        request.json['flag']
    )
    return jsonify({'Mensaje': message})


@app_autor.route("/<int:id>", methods=["DELETE"])
@token_required
def eliminar_autor(id):
    message = serv_autor.delete_autor(id)
    return jsonify({'Mensaje': message})