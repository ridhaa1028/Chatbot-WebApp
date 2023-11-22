from sqlalchemy import Column, Integer, String, Text
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
    



