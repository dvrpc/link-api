from sqlalchemy.orm import Session
from . import models


def get_projects_by_user(db: Session, username: str):
    return db.query(models.Project).filter(models.Project.username == username).all()
