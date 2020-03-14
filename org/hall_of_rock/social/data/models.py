
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PostModel(Base):
    __tablename__ = 'posts'

    id = Column(String, primary_key=True)
    message = Column(String)
    created_time = Column(DateTime)
    full_picture = Column(String)


class AppSettingModel(Base):
    __tablename__ = 'settings'
    name = Column(String, primary_key=True)
    value = Column(String)
