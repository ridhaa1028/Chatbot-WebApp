from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import SectionTally  # Replace 'your_module' with the actual module where models.py is located

# Create an SQLAlchemy engine
engine = create_engine('sqlite:///courses.db')

# Create an SQLAlchemy session
session = Session(engine)

try:
    # Query the database
    course = session.query(SectionTally).first()
    print(course)  # Print the result to check if data is retrieved

except Exception as e:
    print(f"Error: {e}")

finally:
    session.close()  # Close the session
