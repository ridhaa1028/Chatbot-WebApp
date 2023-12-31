from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import CourseBase, InfrastructureBase, EventsBase
from .models_users import Base as UserBase
from .auth import auth, User, login_required, current_user
from flask_jwt_extended import JWTManager
from .auth import auth, User, login_required
from flask_login import LoginManager
from .auth import initialize_jwt, login_manager
from flask_mail import Mail, Message
import requests
import logging
logging.basicConfig(level=logging.DEBUG)



app = Flask(__name__, template_folder='../templates')
app.secret_key = 'your_secret_key'  # Set your secret key here
CORS(app)  # Enable CORS for all routes

# Create an SQLAlchemy engine for general data (courses)
# Create an SQLAlchemy engine
engine = create_engine('sqlite:///courses.db')

# Create an SQLAlchemy session for general data (courses)
# Create an SQLAlchemy session
Session = sessionmaker(bind=engine)

# Create an SQLAlchemy engine for user data
user_data_engine = create_engine('sqlite:///users.db')
UserBase.metadata.bind = user_data_engine

# Create the database and tables
UserBase.metadata.create_all(bind=user_data_engine)

# IDK HOW THIS WORKS LET ME JUST TRY THIS - Muhammad
loc_data_engine = create_engine('sqlite:///infrastructure.db')
events_data_engine = create_engine('sqlite:///events.db')

InfrastructureSession = sessionmaker(bind=loc_data_engine)
EventsSession = sessionmaker(bind=events_data_engine)


InfrastructureBase.metadata.bind = loc_data_engine
InfrastructureBase.metadata.create_all(bind=loc_data_engine)

EventsBase.metadata.bind = events_data_engine
EventsBase.metadata.create_all(bind=events_data_engine)


#################################################
# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587  # Use the appropriate port for your mail server
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ru.profbot@gmail.com'
app.config['MAIL_PASSWORD'] = 'syhf khwh hcrz qzvo'
app.config['MAIL_DEFAULT_SENDER'] = 'ru.profbot@gmail.com'

mail = Mail(app)  # Initialize Flask-Mail


# Initialize Flask-JWT-Extended
initialize_jwt(app)

# Initialize Flask-Login
login_manager.init_app(app)

# Create an SQLAlchemy session for user data
UserSession = sessionmaker(bind=user_data_engine)
app.config['UserSession'] = UserSession

# Register authentication blueprints
app.register_blueprint(auth, url_prefix='/auth')

# Import and add the resources
from .all_data import AllDataResource  # Update with your actual import path
from .data_by_column import DataByColumnResource  # Update with your actual import path
from .catalog_data_by_column import CourseDataByColumnResource
from .events_data_by_column import EventsDataByColumnResource
from .infrastructure_data_by_column import InfrastructureDataByColumnResource
from .create_schedule import ScheduleCreationResource

api = Api(app)
api.add_resource(AllDataResource, '/all_data', resource_class_kwargs={'Session': Session})
api.add_resource(DataByColumnResource, '/data_by_column', resource_class_kwargs={'Session': Session})
api.add_resource(CourseDataByColumnResource, '/catalog_data_by_column', resource_class_kwargs={'Session': Session})
api.add_resource(EventsDataByColumnResource, '/events_data_by_column', resource_class_kwargs={'Session': EventsSession})
api.add_resource(InfrastructureDataByColumnResource, '/infrastructure_data_by_column', resource_class_kwargs={'Session': InfrastructureSession})
api.add_resource(ScheduleCreationResource, '/create_schedule', resource_class_kwargs={'Session': Session})

if __name__ == '__main__':
    app.run(debug=True)

# Home route
@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('index2.html', logged_in=True)
    else:
        return render_template('index.html', logged_in=False)

@app.route('/login')
def login():
    return render_template('test.html', logged_in=True)

@app.route('/User_Guide')
def userGuide():
    if current_user.is_authenticated:
        return render_template('userGuide.html')
    else:
        return render_template('UserGuide2.html')

@app.route('/account')
def account():
    if current_user.is_authenticated:
        return render_template('account.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        # Get email parameters from the request
        recipient = request.json.get('recipient')
        body = request.json.get('body')

        # Check if recipient and body are provided
        if not recipient or not body:
            return jsonify({'error': 'Recipient and body are required'}), 400

        # Create the email message
        msg = Message('Subject', recipients=[recipient])
        msg.body = body

        # Send the email
        mail.send(msg)

        return jsonify({'message': 'Email sent successfully'})
    
    except Exception as e:
        return jsonify({'error': f'Error sending email: {str(e)}'}), 500


