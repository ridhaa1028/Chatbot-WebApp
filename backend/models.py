from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SectionTally(Base):
    __tablename__ = 'section_tally'

    crn = Column(Integer, primary_key=True)
    subj = Column(String(255), nullable=False)
    crse = Column(String(255), nullable=False)
    sect = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    prof = Column(String(255))
    day_beg_end_bldgroom_type = Column(String(255))
    hrs = Column(Integer, nullable=False)
    avail = Column(Integer)

    def __repr__(self):
        return f'<Course {self.crn}>'
    
class Catalog(Base):
    __tablename__ = 'catalog'

    subj = Column(String(255), nullable=False)
    crse = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=False)
    prereq = Column(Text)
    description = Column(Text)
    level = Column(String(255))

    def __repr__(self):
        return f'<Catalog {self.subj} {self.crse}>'
    
class Infrastructure(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    keywords = Column(String(255))
    categories = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    departments = Column(String(255))
    
    def __repr__(self):
        return f'<Location {self.id}:  {self.name}>'

class CurrentEvents(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    host = Column(String(255))
    location = Column(String(255))
    start = Column(DateTime)
    end = Column(DateTime)
    last_modified = Column(DateTime)
    url = Column(String(255))
    
    def __repr__(self):
        return f'<Event {self.id}:  {self.name}>'
