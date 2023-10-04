# app.py

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from scraping import scrape_website_data  # Import your scraping function

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)
api = Api(app)

from model import MyTable

# Add the resource to the API with a route
api.add_resource(MyTableResource, '/api/items/<int:id>')

if __name__ == '__main__':
    # Run the web scraping logic on application startup
    initial_scraping_success = scrape_website_data() #function returns boolean value

    if initial_scraping_success:
        print('Initial data scraping on startup succeeded')
    else:
        print('Initial data scraping on startup failed')

    # Create the database and tables
    db.create_all()
    
    # Start the Flask application
    app.run(debug=True)


