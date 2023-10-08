from flask_restful import Api, Resource, reqparse
from flask import jsonify
#from app import Base  # Import the Base from app.py
from .models import Course  # Import the Course model from models.py

parser = reqparse.RequestParser()
parser.add_argument('column_name', type=str)
parser.add_argument('column_value', type=str)

class DataByColumnResource(Resource):
    def __init__(self, Session):
        self.Session = Session

    def get(self):
        args = parser.parse_args()
        column_name = args['column_name']
        column_value = args['column_value']

        # Define the list of valid column names to prevent SQL injection
        valid_columns = ['crn', 'subj', 'crse', 'sect', 'title', 'prof', 'day_beg_end_bldgroom_type', 'hrs', 'avail']

        # Check if the provided column name is valid
        if column_name in valid_columns:
            # Create a new session for this request
            session = self.Session()

            try:
                # Build the query dynamically using getattr
                query = getattr(Course, column_name) == column_value
                data = session.query(Course).filter(query).all()

                if data:
                    # Format the response to include all columns for each matching course
                    data_list = [{column: getattr(item, column) for column in valid_columns} for item in data]
                    return jsonify(data_list)
                else:
                    return jsonify([])  # Return an empty list if no matching records found
            finally:
                session.close()  # Close the session to release resources
        else:
            return jsonify({"error": "Invalid column name"}), 400  # Return an error for an invalid column name



