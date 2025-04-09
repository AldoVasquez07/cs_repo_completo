from security.connection import PostgreSQLPool
from services.serv_genero import ServGenero
from flask import Blueprint, jsonify
from security.token import token_required


serv_genero = ServGenero(PostgreSQLPool())

app_genero = Blueprint("genero", __name__, url_prefix="/genero")


@app_genero.route("/", methods=["GET"])
@token_required
def get_generos():
    generos = serv_genero.get_generos()
    data = [{"id":g.id, "nombre":g.nombre} for g in generos]
    return jsonify(data)


@app_genero.route("/<int:id>", methods=["GET"])
@token_required
def get_genero(id):
    genero = serv_genero.get_genero(id)
    
    if not genero:
        return jsonify({'Error': 'No existe el registro'})
        
    data = {'id':genero.id, 'nombre':genero.nombre}
    return jsonify(data)


@app_genero.route("/", methods=["POST"])
@token_required
def crear_genero():
    message = serv_genero.insert_genero(
        request.json['nombre']
    )
    return jsonify({'Mensaje': message})


@app_genero.route("/<int:id>", methods=["PUT"])
@token_required
def actualizar_genero(id):
    message = serv_genero.update_genero(
        id,
        request.json['nombre'],
        request.json['flag']
    )
    return jsonify({'Mensaje': message})
    

@app_genero.route("/<int:id>", methods=["DELETE"])
@token_required
def eliminar_autor(id):
    message = serv_genero.delete_genero(id)
    return jsonify({'Mensaje': message})
