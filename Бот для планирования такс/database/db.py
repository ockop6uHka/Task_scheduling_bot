from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Task
from sqlalchemy.exc import SQLAlchemyError

engine = create_engine('postgresql://postgres:postgres@localhost:5432/tasks_db')

Session = sessionmaker(bind=engine)
session = Session()


def add_task(description):
    try:
        task = Task(description=description)
        session.add(task)
        session.commit()
        return task
    except SQLAlchemyError as Er:
        session.rollback()
        raise Er


def delete_task_by_id(task_id):
    try:
        task = session.query(Task).filter_by(id=task_id).first()
        if task:
            session.delete(task)
            session.commit()
            return True
        else:
            return False
    except SQLAlchemyError as Er:
        session.rollback()
        raise Er

def get_all_tasks():
    try:
        tasks = session.query(Task).all()
        return tasks
    except SQLAlchemyError as Er:
        raise Er


def delete_all_tasks():
    try:
        session.query(Task).delete()
        session.commit()
    except SQLAlchemyError as Er:
        session.rollback()
        raise Er