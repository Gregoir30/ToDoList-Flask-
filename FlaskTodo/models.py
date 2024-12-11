from operator import index

from flask_sqlalchemy import SQLAlchemy
from marshmallow.fields import Integer, String, Boolean
from sqlalchemy import column, Column
from sqlalchemy.orm import declarative_base

Base = declarative_base()

db = SQLAlchemy(model_class=Base)

class Task(Base):
    query = None
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    is_done = db.Column(db.Boolean, default=False)