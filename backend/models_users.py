from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

Base = declarative_base()

class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    conversations = relationship('Conversation', backref='author', lazy=True)

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Add this property
    @property
    def is_active(self):
        return True  # Change this condition based on your app's logic

    @property
    def is_authenticated(self):
        return True  # Change this condition based on your app's logic

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

# @app.route('/add_line', methods=['POST'])
# def add_line():
#     data = request.get_json()

#     if 'user_id' not in data or 'content' not in data:
#         return jsonify({'error': 'Missing user_id or content'}), 400

#     user_id = data['user_id']
#     content = data['content']

#     user = User.query.get(user_id)

#     if not user:
#         return jsonify({'error': 'User not found'}), 404

#     conversation = Conversation(content=content, author=user)
#     db.session.add(conversation)
#     db.session.commit()

#     return jsonify({'message': 'Line added successfully'}), 201
