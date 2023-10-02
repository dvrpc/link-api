from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from sqlalchemy import update
from . import models

# Create
# Read


def get_projects_by_user(db: Session, username: str):

    try:
        return db.query(models.Project).filter(
            models.Project.username == username).all()
    except DBAPIError:
        return None

# Update


def rename_segment(db: Session, oldName: str, newName: str, username: str):
    stmt = (
        update(models.Project)
        .where((models.Project.username == username) & (models.Project.seg_name == oldName))
        .values(seg_name=newName)
    )
    db.execute(stmt)
    db.commit()
# Delete
