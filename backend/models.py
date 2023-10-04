from flask_sqlalchemy import SQLAlchemy
from datetime import time  # Import the time class

db = SQLAlchemy()

class MyTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    instructor = db.Column(db.String(255))
    days = db.Column(db.String(255))
    time = db.Column(db.Time)  # Use db.Time for time values

