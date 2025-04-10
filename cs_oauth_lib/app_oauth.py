from controller.control_token import app_token
from flask import Flask


app = Flask(__name__)

app.register_blueprint(app_token)


if __name__ == '__main__':
    app.run(port=5001)