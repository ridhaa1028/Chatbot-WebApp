from flask_restful import Api, Resource
from flask import jsonify
from sqlalchemy.orm import Session
#from app import Base  # Import the Base from app.py
from .models import Course  # Import the Course model from models.py

class AllDataResource(Resource):
    def __init__(self, session: Session):
        self.session = session

    def get(self):
        data = self.session.query(Course).all()
        data_list = [
            {
                'crn': item.crn,
                'subject': item.subj,
                'crse': item.crse,
                'sect': item.sect,
                'title': item.title,
                'prof': item.prof,
                'day_beg_end_bldgroom_type': item.day_beg_end_bldgroom_type,
                'hrs': item.hrs,
                'avail': item.avail
            }
            for item in data
        ]
        return jsonify(data_list)



