from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models_users import User, Base
from flask import jsonify

auth = Blueprint('auth', __name__)

engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(bind=engine)
UserSession = sessionmaker(bind=engine)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(auth)

# Initialize Flask-JWT-Extended
jwt = JWTManager()

# Function to initialize JWT later when the app is created
def initialize_jwt(app):
    jwt.init_app(app)

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return UserSession().query(User).get(int(user_id))

# New API route to get current user information
@auth.route('/api/current_user', methods=['GET'])
@login_required
def get_current_user():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email
    })

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        session = UserSession()
        user = session.query(User).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('home'))

        flash('Login unsuccessful. Please check your username and password.', 'danger')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('home'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        session = UserSession()
        existing_user = session.query(User).filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            flash('Username or email already exists. Please choose a different one.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, email=email, password=generate_password_hash(password))
        session.add(new_user)
        session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

# JWT token generation route
@auth.route('/get_token', methods=['POST'])
@login_required
def get_token():
    access_token = create_access_token(identity=current_user.id)
    return {'access_token': access_token}





