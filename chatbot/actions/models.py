from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

InfrastructureBase = declarative_base()
EventsBase = declarative_base()

class Infrastructure(InfrastructureBase):
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

class CurrentEvents(EventsBase):
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