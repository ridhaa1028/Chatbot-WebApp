# Represents ORM Model for Database
# Has two queries. One for retriving all possible sections to take
# Second for getting details of 1 possible schedule (Represented by crns)

#

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_

Base = declarative_base()
class Course(Base):
    __tablename__ = 'section_tally'

    crn = Column(Integer, primary_key=True)
    subj = Column(String(255))
    crse = Column(String(255))
    sect = Column(String(255))
    title = Column(String(255))
    prof = Column(String(255))
    day_beg_end_bldgroom_type = Column(String(255))
    hrs = Column(Integer)
    avail = Column(Integer)

    def __repr__(self):
        return f'<Course {self.crn}>'
    
# Setup the database connection
DATABASE_URL = "sqlite:///../backend/courses.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def fetch_course(course_list):
    with SessionLocal() as session:
        # Query based on the list of tuples
        results = session.query(Course).filter(or_(*(and_(Course.subj == subj, Course.crse == crse) for subj, crse in course_list))).all()
        session.close()
        return results

def detail_schedule(list_of_crns):
    with SessionLocal() as session:
        results = session.query(Course).filter(or_(*(Course.crn == crn for crn in list_of_crns))).all()
        session.close()
        return results