from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from sqlalchemy import update, func
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


def get_geoms_by_user_study(db: Session, username: str, study: str, model):

    try:
        return db.query(func.ST_AsGeoJSON(func.ST_ForceRHR(func.ST_Transform(model.geom, 4326))).label('geometry')).\
            select_from(models.UserSegments).\
            join(model, models.UserSegments.id == model.id).\
            filter(models.UserSegments.username == username).\
            filter(models.UserSegments.seg_name == study).\
            first()

    except DBAPIError as e:
        print(f"DBAPIError occurred: {e}")
        print(f"Statement: {e.statement}")
        print(f"Params: {e.params}")
        return None


def get_segment_geoms_by_user_study(db: Session, username: str, study: str, model):

    try:
        return db.query(func.ST_AsGeoJSON(func.ST_Transform(model.geom, 4326)).label('geometry')).\
            select_from(models.UserSegments).\
            filter(models.UserSegments.id == model.id).\
            filter(models.UserSegments.username == username).\
            filter(models.UserSegments.seg_name == study).\
            first()

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
