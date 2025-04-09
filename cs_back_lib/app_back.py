from flask import Flask
from controller.control_autor import app_autor
from controller.control_genero import app_genero
from controller.control_libro import app_libro
from controller.control_autor_libro import app_autor_libro
from controller.control_libro_genero import app_libro_genero

app = Flask(__name__)

app.register_blueprint(app_autor)
app.register_blueprint(app_genero)
app.register_blueprint(app_libro)
app.register_blueprint(app_autor_libro)
app.register_blueprint(app_libro_genero)



if __name__=="__main__":
    app.run(debug=True, port=5000)