from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base  = declarative_base()

class Admin(Base):
    __tablename__ = 'admin'
    id  = Column(Integer, primary_key=True, index=True)
    admin_name = Column(String)
    competition_id = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class Applicant(Base):
    __tablename__ = 'applicant'
    id = Column(Integer, primary_key=True)
    applicant_name = Column(String)
    admin_id = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

class Competition(Base):
    __tablename__ = 'competition'
    id = Column(Integer, primary_key=True)
    competition_name = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())