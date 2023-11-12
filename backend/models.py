from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Course(Base):
    __tablename__ = 'courses'

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
    



