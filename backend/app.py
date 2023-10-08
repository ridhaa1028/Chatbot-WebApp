# backend/app.py
#from flask import Flask
#from flask_restful import Api
#from flask_sqlalchemy import SQLAlchemy

#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
#db = SQLAlchemy(app)
#api = Api(app)

# Import and add the resources
#from api.all_data import AllDataResource
#from api.data_by_column import DataByColumnResource

#api.add_resource(AllDataResource, '/api/all_data')
#api.add_resource(DataByColumnResource, '/api/data_by_column')

#if __name__ == '__main__':
#    app.run(debug=True)

from flask import Flask
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from .models import Base  # Import Base from your models.py

app = Flask(__name__)

# Create an SQLAlchemy engine
engine = create_engine('sqlite:///courses.db')

# Create an SQLAlchemy session
Session = sessionmaker(bind=engine)

# Import and add the resources
from .all_data import AllDataResource  # Update with your actual import path
from .data_by_column import DataByColumnResource  # Update with your actual import path

api = Api(app)
api.add_resource(AllDataResource, '/all_data', resource_class_kwargs={'Session': Session})
api.add_resource(DataByColumnResource, '/data_by_column', resource_class_kwargs={'Session': Session})

if __name__ == '__main__':
    app.run(debug=True)



