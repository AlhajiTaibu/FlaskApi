from flask import Flask
from flask_jwt_extended import JWTManager
import os
from demo.models import db
from dotenv import load_dotenv
load_dotenv()

jwt = JWTManager()

debug_mode = os.getenv('DEBUG')


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['DEBUG'] = debug_mode
    if debug_mode:
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/projectdb"
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    from . import auth
    app.register_blueprint(auth.bp)

    return app
