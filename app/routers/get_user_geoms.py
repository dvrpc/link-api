from fastapi import APIRouter, Depends, Query
from dotenv import load_dotenv
from data_structures import schemas, database, crud, models
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import json

load_dotenv()

router = APIRouter()


@router.get("/get_user_study_geoms/", response_model=schemas.UserGeoms)
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
        response.blobs = json.loads(blobs.geom)
    else:
        response.blobs = schemas.FeatureModel(
            type=None, geom=None, properties=None)
    if buffers:
        response.buffers = json.loads(buffers.geom)
    else:
        response.buffers = schemas.FeatureModel(
            type=None, geom=None, properties=None)
    if isochrones:
        response.isochrones = json.loads(isochrones.geom)
    else:
        response.isochrones = schemas.FeatureModel(
            type=None, geom=None, properties=None)

    if response is None:
        return JSONResponse(content={"geometries": ["No geometries exist!"]})
    else:
        geojson_r = {
            "blobs": response.blobs,
            "isochrones": response.isochrones,
            "buffers": response.buffers,
        }

        print(geojson_r)
        return geojson_r
