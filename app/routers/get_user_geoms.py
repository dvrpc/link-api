from fastapi import APIRouter, Depends, Query
from dotenv import load_dotenv
from data_structures import schemas, database, crud, models
from sqlalchemy.orm import Session
import json
from fastapi.responses import JSONResponse
import os
import zipfile
from fastapi.responses import FileResponse
import tempfile
import shutil

load_dotenv()

router = APIRouter()


def fetch_user_study_geoms(username: str, study: str, db: Session):
    blobs = crud.get_geoms_by_user_study(db, username, study, models.UserBlobs)
    buffers = crud.get_geoms_by_user_study(
        db, username, study, models.UserBuffers)
    isochrones = crud.get_geoms_by_user_study(
        db, username, study, models.UserIsochrones)

    return blobs, buffers, isochrones


def fetch_segment_geoms(username: str, study: str, db: Session):
    segments = crud.get_segment_geoms_by_user_study(
        db, username, study, models.UserSegments)

    return segments


def format_as_feature_collection(blobs, buffers, isochrones):
    response = schemas.UserGeoms()
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
            type="Feature", geometry=None, properties=None, id="buffers")
    if isochrones:
        geom = json.loads(isochrones.geometry)
        response.isochrones = schemas.FeatureModel(
            type='Feature', geometry=schemas.Geometry(type=geom['type'], coordinates=geom['coordinates']), properties=None, id=("isochrones"))
    else:
        response.isochrones = schemas.FeatureModel(
            type="Feature", geometry=None, properties=None, id="isochrones")

    if not blobs and not buffers and not isochrones:
        # No geometries found, return an error response
        return JSONResponse(
            status_code=404,
            content={
                "message": "No geometries found for the specified user and study."}
        )

    feature_collection = schemas.FeatureCollection(
        features=[response.blobs, response.isochrones, response.buffers])
    return feature_collection


def save_as_geojson_and_zip(blobs, buffers, isochrones, username, study, segments):
    final_zip_path = f"{study}_{username}_link_tool_geoms.zip"

    with tempfile.TemporaryDirectory() as temp_dir:
        geojson_files = []
        for geom_type, geom in [('blobs', blobs), ('buffers', buffers), ('isochrones', isochrones), ('segments', segments)]:
            if geom:
                file_path = os.path.join(
                    temp_dir, f"{geom_type}_{username}_{study}.geojson")
                with open(file_path, 'w') as file:
                    json.dump(
                        {"type": "Feature", "geometry": json.loads(geom.geometry)}, file)
                geojson_files.append(file_path)

        if not geojson_files:
            raise ValueError("No geometries found.")

        zip_filename = os.path.join(temp_dir, final_zip_path)
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file in geojson_files:
                zipf.write(file, os.path.basename(file))

        shutil.copy(zip_filename, final_zip_path)

    return final_zip_path


@router.get("/get_user_study_geoms/", response_model=schemas.FeatureCollection)
def user_study_geoms(username: str, study: str, schema: str = Query(...), db: Session = Depends(database.get_db_for_schema)):
    blobs, buffers, isochrones = fetch_user_study_geoms(username, study, db)
    return format_as_feature_collection(blobs, buffers, isochrones)


@router.get("/download_user_study_geoms/")
def download_user_study_geoms(username: str, study: str, schema: str = Query(...), db: Session = Depends(database.get_db_for_schema)):
    blobs, buffers, isochrones = fetch_user_study_geoms(username, study, db)
    segments = fetch_segment_geoms(username, study, db)
    zip_filename = save_as_geojson_and_zip(
        blobs, buffers, isochrones, username, study, segments)
    return FileResponse(zip_filename, media_type='application/octet-stream', filename=zip_filename)
