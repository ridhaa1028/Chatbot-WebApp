# Import request
from flask import Blueprint, jsonify, request, current_app
from sqlalchemy.exc import IntegrityError
from .models_users import User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/register', methods=['POST'])
def register():
    data = request.form
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    new_user = User(username=data['username'], email=data['email'], password=hashed_password)

    session = current_app.config['UserSession']()
    try:
        session.add(new_user)
        session.commit()
        access_token = create_access_token(identity=new_user.id)
        return jsonify(access_token=access_token, message="Registration successful"), 201
    except IntegrityError:
        session.rollback()
        return jsonify(message="User already exists"), 400
    finally:
        session.close()

@auth.route('/login', methods=['POST'])
def login():
    data = request.form  # Use request.form to get form data
    user = User.query.filter_by(username=data['username']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token, message="Login successful"), 200
    else:
        return jsonify(message="Invalid username or password"), 401

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200



