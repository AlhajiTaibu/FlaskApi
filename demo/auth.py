from flask import (
    Blueprint, request, session
)
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from demo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('POST',))
def register():
    error = None
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                user = User(
                    email=email,
                    password=generate_password_hash(password)
                )
                db.session.add(user)
                db.session.commit()
            except db.IntegrityError:
                error = f"User {email} is already registered."
            else:
                return {
                    "code": 201,
                    "message": "User registered successfully"
                }

        return {
            "code": 400,
            "message": error
        }
    return {
        "code": 400,
        "message": "Only POST request is expected"
    }


@bp.route('/login', methods=('POST',))
def login():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        error = None
        user = User.query.filter_by(email=email).first()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id

            access_token = create_access_token(identity=user.id)

            return {
                "code": 200, 'token': access_token, 'message': 'Login successful'
            }
        return {
            "code": 400,
            "message": error
        }

    return {
        "code": 400,
        "message": "Only POST request is expected"
    }


@bp.route('/users', methods=('GET',))
@jwt_required()
def users():
    userz = User.query.all()
    return {
        "code": 200,
        "data": [user.to_dict() for user in userz]
    }
