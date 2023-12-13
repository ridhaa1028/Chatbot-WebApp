from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin
from datetime import datetime, timedelta
import random 
import string

Base = declarative_base()

class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    reset_code = Column(String(32), nullable=True)
    reset_code_expiration = Column(DateTime, nullable=True)
    conversations = relationship('Conversation', backref='author', lazy=True)
    
    def generate_reset_code(self):
        self.reset_code = generate_random_code()
        self.reset_code_expiration = datetime.now() + timedelta(minutes=15)

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    is_user_message = Column(Boolean, nullable=False) 
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



def generate_random_code(length=32):
    """Generate a random code of the specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))