from fastapi import APIRouter, Depends, Query
from dotenv import load_dotenv
from data_structures import schemas, database, crud, models
from sqlalchemy.orm import Session
import json

load_dotenv()

router = APIRouter()


@router.get("/get_user_segment/", response_model=schemas.FeatureCollection)
def user_study_geoms(
        username: str,
        study: str,
        schema: str = Query(...,
                            description="The schema to use (lts or sidewalk)"),
        db: Session = Depends(database.get_db_for_schema)):
    db: Session = database.get_db_for_schema(schema)

    response = schemas.UserSegments()
    segments = crud.get_segment_geoms_by_user_study(
        db, username, study, models.UserSegments)

    if segments:
        geom = json.loads(segments.geometry)
        response.segments = schemas.FeatureModel(
            type="Feature", geometry=schemas.Geometry(type=geom['type'], coordinates=geom['coordinates']), properties=None, id="segments")
    else:
        response.segments = schemas.FeatureModel(
            type="Feature", geometry=None, properties=None, id="segments")

    feature_collection = schemas.FeatureCollection(
        features=[response.segments])
    return feature_collection
