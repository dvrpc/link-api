import re
from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from sqlalchemy import update, func, or_, and_
from . import models

# Create
# Read


def get_projects_by_user(db: Session, username: str):
    try:
        return (
            db.query(models.UserSegments)
            .filter(models.UserSegments.username == username)
            .filter(
                or_(
                    models.UserSegments.deleted.is_(False),
                    models.UserSegments.deleted.is_(None),
                )
            )
            .all()
        )
    except DBAPIError as e:
        print(f"DBAPIError occurred: {e}")
        print(f"Statement: {e.statement}")
        print(f"Params: {e.params}")
        return None


def get_all_projects(
    db: Session,
):
    try:
        return db.query(models.UserSegments).all()
    except DBAPIError as e:
        print(f"DBAPIError occurred: {e}")
        print(f"Statement: {e.statement}")
        print(f"Params: {e.params}")
        return None


def get_project_by_name(db: Session, study_name: str, username: str):
    return (
        db.query(models.UserSegments)
        .filter(models.UserSegments.seg_name == study_name)
        .filter(models.UserSegments.username == username)
        .first()
    )


def get_geoms_by_user_study(db: Session, username: str, study: str, model):
    try:
        return (
            db.query(
                func.ST_AsGeoJSON(
                    func.ST_ForceRHR(func.ST_Transform(model.geom, 4326))
                ).label("geometry")
            )
            .select_from(models.UserSegments)
            .join(model, models.UserSegments.id == model.id)
            .filter(models.UserSegments.username == username)
            .filter(models.UserSegments.seg_name == study)
            .first()
        )

    except DBAPIError as e:
        print(f"DBAPIError occurred: {e}")
        print(f"Statement: {e.statement}")
        print(f"Params: {e.params}")
        return None


def get_segment_geoms_by_user_study(db: Session, username: str, study: str, model):
    try:
        return (
            db.query(
                func.ST_AsGeoJSON(func.ST_Transform(model.geom, 4326)).label("geometry")
            )
            .select_from(models.UserSegments)
            .filter(models.UserSegments.id == model.id)
            .filter(models.UserSegments.username == username)
            .filter(models.UserSegments.seg_name == study)
            .first()
        )

    except DBAPIError as e:
        print(f"DBAPIError occurred: {e}")
        print(f"Statement: {e.statement}")
        print(f"Params: {e.params}")
        return None


# Update


def rename_segment(db: Session, oldName: str, newName: str, username: str):
    newName = re.sub(r"[^a-zA-Z0-9 ]", "", newName)
    exists = (
        db.query(models.UserSegments.seg_name).filter_by(seg_name=newName).first()
        is not None
    )
    if not exists:
        stmt = (
            update(models.UserSegments)
            .where(
                (models.UserSegments.username == username)
                & (models.UserSegments.seg_name == oldName)
            )
            .values(seg_name=newName)
        )
        db.execute(stmt)
        db.commit()
    else:
        raise ValueError("Segment name was already used, try a different name.")


def share_study(db: Session, username: str, seg_name: str, share: bool):
    stmt = (
        update(models.UserSegments)
        .where(
            and_(
                models.UserSegments.username == username,
                models.UserSegments.seg_name == seg_name,
            )
        )
        .values(shared=share)
    )
    db.execute(stmt)
    db.commit()


# Delete


def delete_study(db: Session, username: str, seg_name: str):
    stmt = (
        update(models.UserSegments)
        .where(
            and_(
                models.UserSegments.username == username,
                models.UserSegments.seg_name == seg_name,
            )
        )
        .values(deleted=True)
    )
    db.execute(stmt)
    db.commit()
