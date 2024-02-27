import json
import os
from typing_extensions import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from data_structures import crud, database, models, schemas
from . import basic_auth

load_dotenv()
URL_ROOT = os.environ.get("URL_ROOT", "")

router = APIRouter()


def get_segment_geometries(username: str, study: str, db: Session):
    # Your logic to fetch segment geometries
    response = schemas.UserSegments()
    segments = crud.get_segment_geoms_by_user_study(db, username, study, models.UserSegments)

    if segments:
        geom = json.loads(segments.geometry)
        response.segments = schemas.FeatureModel(
            type="Feature",
            geometry=schemas.Geometry(type=geom["type"], coordinates=geom["coordinates"]),
            properties=None,
            id="segments",
        )
    else:
        response.segments = schemas.FeatureModel(
            type="Feature", geometry=None, properties=None, id="segments"
        )

    feature_collection = schemas.FeatureCollection(features=[response.segments])
    return feature_collection


@router.get(f"{URL_ROOT}/get_user_segment", response_model=schemas.FeatureCollection)
def user_study_segment_geoms(
    basic_auth: Annotated[str, Depends(basic_auth)],
    username: str,
    study: str,
    schema: str = Query(..., description="The schema to use (lts or sidewalk)"),
    db: Session = Depends(database.get_db_for_schema),
):
    return get_segment_geometries(username, study, db)
