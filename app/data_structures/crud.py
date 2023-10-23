from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from sqlalchemy import update
from . import models

# Create
# Read


def get_projects_by_user(db: Session, username: str):

    try:
        return db.query(models.UserSegments).filter(
            models.UserSegments.username == username).all()
    except DBAPIError as e:
        print(f"DBAPIError occurred: {e}")
        print(f"Statement: {e.statement}")
        print(f"Params: {e.params}")
        return None

# Update


def rename_segment(db: Session, oldName: str, newName: str, username: str):
    stmt = (
        update(models.UserSegments)
        .where((models.UserSegments.username == username) & (models.UserSegments.seg_name == oldName))
        .values(seg_name=newName)
    )
    db.execute(stmt)
    db.commit()
# Delete
