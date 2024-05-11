from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Task(id={self.id}, description={self.description}, created_at={self.created_at})>"