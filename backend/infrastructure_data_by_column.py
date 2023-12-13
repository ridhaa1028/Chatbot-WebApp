from flask_restful import Api, Resource, reqparse
from flask import jsonify
from .models import Infrastructure

parser = reqparse.RequestParser()
parser.add_argument('column_name', type=str, action='append')
parser.add_argument('column_value', type=str, action='append')

class InfrastructureDataByColumnResource(Resource):
    def __init__(self, Session):
        self.Session = Session

    def get(self):
        args = parser.parse_args()
        column_names = args['column_name']
        column_values = args['column_value']

        if not column_names or not column_values:
            return jsonify({"error": "You must provide at least one column_name and one column_value."}), 400

        # Define the list of valid column names to prevent SQL injection
        valid_columns = ['id','name', 'description', 'keywords', 'categories','latitude', 'longitude', 'departments'] 

        # Validate the provided column names
        invalid_columns = [col for col in column_names if col not in valid_columns]

        if invalid_columns:
            return jsonify({"error": f"Invalid column names: {', '.join(invalid_columns)}"}), 400

        # Create a new session for this request
        session = self.Session()

        try:
            # Build the query dynamically using getattr
            filters = [getattr(Infrastructure, col) == val for col, val in zip(column_names, column_values)]
            data = session.query(Infrastructure).filter(*filters).all()

            if data:
                # Format the response to include all columns for each matching course
                data_list = [{column: getattr(item, column) for column in valid_columns} for item in data]
                return jsonify(data_list)
            else:
                return jsonify([])  # Return an empty list if no matching records found
        finally:
            session.close()  # Close the session to release resources