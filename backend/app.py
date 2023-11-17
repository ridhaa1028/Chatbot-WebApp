from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  # Import sessionmaker
from .models import Base as CourseBase  # Import Base from your models.py
from .models_users import Base as UserBase  # Import the Base from models_users.py
from flask_jwt_extended import JWTManager
from .auth import auth

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up JWT for user authentication
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

# Create an SQLAlchemy engine for general data (courses)
courses_data_engine = create_engine('sqlite:///courses.db')
CourseBase.metadata.bind = courses_data_engine

# Create an SQLAlchemy session for general data (courses)
CourseSession = sessionmaker(bind=courses_data_engine)

# Create an SQLAlchemy engine for user data
user_data_engine = create_engine('sqlite:///users.db')
UserBase.metadata.bind = user_data_engine

# Create the database and tables
UserBase.metadata.create_all(bind=user_data_engine)

# Create an SQLAlchemy session for user data
UserSession = sessionmaker(bind=user_data_engine)
app.config['UserSession'] = UserSession

# Register authentication blueprints
app.register_blueprint(auth, url_prefix='/auth')

# Import and add the resources
from .all_data import AllDataResource  # Update with your actual import path
from .data_by_column import DataByColumnResource  # Update with your actual import path

api = Api(app)
api.add_resource(AllDataResource, '/all_data', resource_class_kwargs={'Session': CourseSession})
api.add_resource(DataByColumnResource, '/data_by_column', resource_class_kwargs={'Session': CourseSession})

if __name__ == '__main__':
    app.run(debug=True)




