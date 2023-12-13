from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, g
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .models_users import User, Conversation, Base
from datetime import datetime, timedelta
import requests
import traceback

auth = Blueprint('auth', __name__)

engine = create_engine('sqlite:///users.db', connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(bind=engine)
UserSession = scoped_session(sessionmaker(bind=engine))

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
    return UserSession.query(User).get(int(user_id))

# Teardown request to ensure session is closed after each request
@auth.teardown_request
def teardown_request(exception=None):
    if hasattr(g, 'user_session'):
        g.user_session.remove()

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

        try:
            user = UserSession.query(User).filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful.', 'success')
                return redirect(url_for('home'))

            flash('Login unsuccessful. Please check your username and password.', 'danger')
        except Exception as e:
            print(f"Error during login: {e}")
        finally:
            if hasattr(g, 'user_session'):
                g.user_session.remove()

    return jsonify({'success': False, 'message': 'Invalid username or password.'})

@auth.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        flash('Logout successful.', 'success')
        return redirect(url_for('home'))
    except Exception as e:
        print(f"Error during logout: {e}")
    finally:
        if hasattr(g, 'user_session'):
            g.user_session.remove()

@auth.route('/register', methods=['POST'])
def register():
    try:
        username = request.form['new-username']
        email = request.form['email']
        password = request.form['new-password']

        existing_user = UserSession.query(User).filter((User.username == username) | (User.email == email)).first()

        if existing_user:
            return jsonify({'success': False, 'message': 'Username or email already exists. Please choose a different one.'})

        new_user = User(username=username, email=email, password=generate_password_hash(password))
        UserSession.add(new_user)
        UserSession.commit()

        return jsonify({'success': True, 'message': 'Registration successful. Please log in.'})
    except Exception as e:
        print(f"Error during registration: {e}")
        return jsonify({'success': False, 'message': 'An error occurred during registration.'})
    finally:
        if hasattr(g, 'user_session'):
            g.user_session.remove()

# JWT token generation route
@auth.route('/get_token', methods=['POST'])
@login_required
def get_token():
    access_token = create_access_token(identity=current_user.id)
    return {'access_token': access_token}

@auth.route('/add_line_to_conversation', methods=['POST'])
@login_required
def add_line_to_conversation():
    try:
        data = request.get_json()

        content = data.get('content')
        is_user_message = data.get('is_user_message')

        if content is None or is_user_message is None:
            return jsonify({'error': 'Missing or invalid parameters'}), 400

        # Check if the provided 'is_user_message' value is a valid boolean
        if not isinstance(is_user_message, bool):
            return jsonify({'error': 'Invalid value for is_user_message'}), 400

        # Create a new conversation entry
        new_conversation = Conversation(content=content, is_user_message=is_user_message, author=current_user)

        # Add the conversation and commit the changes
        UserSession.add(new_conversation)
        UserSession.commit()

        return jsonify({'message': 'Line added to the conversation successfully'}), 201
    except Exception as e:
        print(f"Error during adding line to conversation: {e}")
        return jsonify({'error': 'An error occurred during adding line to conversation'}), 500
    finally:
        if hasattr(g, 'user_session'):
            g.user_session.remove()

@auth.route('/get_conversations', methods=['GET'])
@login_required
def get_conversations():
    try:
        # Query conversations for the current user, ordered by id
        user_conversations = (
            UserSession()
            .query(Conversation)
            .filter_by(user_id=current_user.id)
            .order_by(Conversation.id)
            .all()
        )

        # Convert conversations to a list of dictionaries
        conversations_data = [
            {
                'id': conversation.id,
                'content': conversation.content,
                'is_user_message': conversation.is_user_message,
            }
            for conversation in user_conversations
        ]

        return jsonify({'conversations': conversations_data})

    except Exception as e:
        print(f"Error during retrieving conversations: {e}")
        return jsonify({'error': 'An error occurred during retrieving conversations'}), 500
    finally:
        if hasattr(g, 'user_session'):
            g.user_session.remove()

@auth.route('/delete_all_conversations', methods=['DELETE'])
@login_required
def delete_all_conversations():
    try:
        # Delete all conversations for the current user
        UserSession.query(Conversation).filter_by(user_id=current_user.id).delete()

        # Commit the changes
        UserSession.commit()

        return jsonify({'message': 'All conversations deleted successfully'})
    except Exception as e:
        print(f"Error during deleting conversations: {e}")
        return jsonify({'error': 'An error occurred during deleting conversations'}), 500
    finally:
        if hasattr(g, 'user_session'):
            g.user_session.remove()

@auth.route('/change_password', methods=['POST'])
@login_required
def change_password():
    try:
        data = request.get_json()

        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if current_password is None or new_password is None:
            return jsonify({'error': 'Missing or invalid parameters'}), 400

        user = UserSession.query(User).filter_by(id=current_user.id).first()

        if user and check_password_hash(user.password, current_password):
            # Change the user's password to the new password
            user.password = generate_password_hash(new_password)

            # Commit the changes
            UserSession.commit()

            return jsonify({'message': 'Password changed successfully'}), 200
        else:
            return jsonify({'error': 'Current password is incorrect'}), 401

    except Exception as e:
        print(f"Error during password change: {e}")
        return jsonify({'error': 'An error occurred during password change'}), 500
    finally:
        if hasattr(g, 'user_session'):
            g.user_session.remove()

@auth.route('/password_reset_request', methods=['POST'])
def password_reset_request():
    try:
        data = request.get_json()
        email = data.get('email')

        if email is None:
            return jsonify({'error': 'Missing email parameter'}), 400

        user = UserSession.query(User).filter_by(email=email).first()

        if user:
            user.generate_reset_code()
            UserSession.commit()

            # Send reset email
            reset_email_body = f"Here is your reset code: {user.reset_code}"
            send_reset_email(user.email, reset_email_body)

            return jsonify({'message': 'Password reset email sent successfully'}), 200
        else:
            return jsonify({'error': 'User with the provided email not found'}), 404
    except Exception as e:
        print(f"Error during password reset request: {e}")
        return jsonify({'error': 'An error occurred during password reset request'}), 500
    finally:
        if hasattr(g, 'user_session'):
            g.user_session.remove()

@auth.route('/password_reset_verify', methods=['POST'])
def password_reset_verify():
    try:
        print("Step 1: Start password reset verification process")
        
        data = request.get_json(force=True)
        print(f"Step 2: Received JSON data: {data}")

        email = data.get('email')
        new_password = data.get('new_password')
        reset_code = data.get('reset_code')
        print(f"Step 3: Extracted email, new_password, reset_code: {email}, {new_password}, {reset_code}")

        if email is None or new_password is None or reset_code is None:
            print("Step 4: Missing or invalid parameters. Returning 400 error.")
            return jsonify({'error': 'Missing or invalid parameters'}), 400

        user = UserSession.query(User).filter_by(email=email).first()
        print(f"Step 5: Queried user: {user}")

        if user and user.reset_code == reset_code and user.reset_code_expiration > datetime.now():
            print("Step 6: Valid reset code. Changing the user's password.")
            
            # Change the user's password to the new password
            user.password = generate_password_hash(new_password)

            # Clear the reset code fields
            user.reset_code = None
            user.reset_code_expiration = None

            # Commit the changes
            UserSession.commit()

            print("Step 7: Password changed successfully. Returning 200.")
            return jsonify({'message': 'Password changed successfully'}), 200
        else:
            print("Step 8: Invalid reset code or expired. Returning 401 error.")
            return jsonify({'error': 'Invalid reset code or expired'}), 401
    except Exception as e:
        print(f"Step 9: Error during password reset verification: {e}")
        traceback.print_exc()
        return jsonify({'error': f'An error occurred during password reset verification: {str(e)}'}), 500
    finally:
        if hasattr(g, 'user_session'):
            g.user_session.remove()
            print("Step 10: Removed user session (if present).")

# Helper function to send email using the /send_email API route
def send_reset_email(recipient, body):
    try:
        # Send the email using the /send_email API route
        response = requests.post(
            'http://localhost:5000/send_email',
            json={'recipient': recipient, 'body': body}
        )

        if response.status_code != 200:
            print(f"Error sending reset email: {response.json()}")

    except Exception as e:
        print(f"Error sending reset email: {e}")