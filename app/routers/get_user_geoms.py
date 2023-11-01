from fastapi import APIRouter, Depends, Query
from dotenv import load_dotenv
from data_structures import schemas, database, crud, models
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import json

load_dotenv()

router = APIRouter()


@router.get("/get_user_study_geoms/", response_model=schemas.FeatureCollection)
def user_study_geoms(
        username: str,
        study: str,
        schema: str = Query(...,
                            description="The schema to use (lts or sidewalk)"),
        db: Session = Depends(database.get_db_for_schema)):
    db: Session = database.get_db_for_schema(schema)

    response = schemas.UserGeoms()

    blobs = crud.get_geoms_by_user_study(
        db, username, study, models.UserBlobs)

    buffers = crud.get_geoms_by_user_study(
        db, username, study, models.UserBuffers)
    isochrones = crud.get_geoms_by_user_study(
        db, username, study, models.UserIsochrones)

    if blobs:
        geom = json.loads(blobs.geometry)
        response.blobs = schemas.FeatureModel(
            type="Feature", geometry=schemas.Geometry(type=geom['type'], coordinates=geom['coordinates']), properties=None, id="blobs")
    else:
        response.blobs = schemas.FeatureModel(
            type="Feature", geometry=None, properties=None, id="blobs")
    if buffers:
        geom = json.loads(buffers.geometry)
        response.buffers = schemas.FeatureModel(
            type="Feature", geometry=schemas.Geometry(type=geom['type'], coordinates=geom['coordinates']), properties=None, id="buffers")
    else:
        response.buffers = schemas.FeatureModel(
            type="Feature", geometry=None, properties=None, id="blobs")
    if isochrones:
        geom = json.loads(isochrones.geometry)
        response.isochrones = schemas.FeatureModel(
            type='Feature', geometry=schemas.Geometry(type=geom['type'], coordinates=geom['coordinates']), properties=None, id=("isochrones"))
    else:
        response.isochrones = schemas.FeatureModel(
            type="Feature", geometry=None, properties=None, id="blobs")

    feature_collection = schemas.FeatureCollection(
        features=[response.blobs, response.isochrones, response.buffers])
    return feature_collection
