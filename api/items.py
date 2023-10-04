# backend/api/items.py

from flask_restful import Resource, reqparse
from model import MyTable  # Import your MyTable model class

# Define a resource for your database table (RESTful API endpoint)
class MyTableResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, help='Filter by class name')

    def get(self, id=None):
        args = self.parser.parse_args()
        name_filter = args['name']

        if id is not None:
            # Retrieve a single item by ID
            item = MyTable.query.get(id)
            if item:
                return {
                    'id': item.id,
                    'name' : item.name,
                    'instructor': item.instructor,
                    'days': item.days,
                    'time': item.time
                }
            else:
                return {'message': 'Item not found'}, 404
        else:
            # Filter items by name if name filter is provided
            query = MyTable.query
            if name_filter:
                query = query.filter_by(MyTable.name.ilike(f'%{name_filter}%'))  # Case-insensitive search

            items = query.all()

            if items:
                return [
                    {
                        'id': item.id,
                        'name' : item.name,
                        'instructor': item.instructor,
                        'days': item.days,
                        'time': item.time
                    }
                    for item in items
                ]
            else:
                return {'message': 'No items found'}, 404

