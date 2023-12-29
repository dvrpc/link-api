from fastapi import APIRouter, Depends, Query, BackgroundTasks
from dotenv import load_dotenv
from data_structures import schemas, database, crud, models
from sqlalchemy.orm import Session
import json
from fastapi.responses import JSONResponse
import os
import zipfile
from fastapi.responses import FileResponse
import tempfile

load_dotenv()

router = APIRouter()


def remove_file_later(path: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(os.remove, path)


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


def save_as_geojson_and_zip(blobs, buffers, isochrones, segments, username, study):
    zip_temp_path = tempfile.mktemp(suffix=".zip")

    with zipfile.ZipFile(zip_temp_path, 'w') as zipf:
        for geom_type, geom in [('blobs', blobs), ('buffers', buffers), ('isochrones', isochrones), ('segments', segments)]:
            if geom:
                file_path = f"{geom_type}_{username}_{study}.geojson"
                with open(file_path, 'w') as file:
                    json.dump(
                        {"type": "Feature", "geometry": json.loads(geom.geometry)}, file)
                zipf.write(file_path, os.path.basename(file_path))
                os.remove(file_path)

        text_file_name = "readme.txt"
        with open(text_file_name, 'w') as text_file:
            text_file.write("Blobs are the islands formed by the low stress network, either LTS 1 and 2 roads, or existing sidewalks. \n\nSegments are the geometries you created for this study. This is the only geojson that can be re-uploaded into the Link tool- other shapes will not work. Only lines. \n\nBuffers are buffers around your study segment, which grab any touching islands and add them to the analysis.")
        zipf.write(text_file_name, os.path.basename(text_file_name))
        os.remove(text_file_name)

    return zip_temp_path


@router.get("/get_user_study_geoms/", response_model=schemas.FeatureCollection)
def user_study_geoms(username: str, study: str, schema: str = Query(...), db: Session = Depends(database.get_db_for_schema)):
    blobs, buffers, isochrones = fetch_user_study_geoms(username, study, db)
    return format_as_feature_collection(blobs, buffers, isochrones)


@router.get("/download_user_study_geoms/")
async def download_user_study_geoms(username: str, study: str, schema: str = Query(...), db: Session = Depends(database.get_db_for_schema), background_tasks: BackgroundTasks = BackgroundTasks()):
    blobs, buffers, isochrones = fetch_user_study_geoms(username, study, db)
    segments = fetch_segment_geoms(username, study, db)
    zip_temp_path = save_as_geojson_and_zip(
        blobs, buffers, isochrones, segments, username, study)

    background_tasks.add_task(os.remove, zip_temp_path)

    return FileResponse(path=zip_temp_path, filename=os.path.basename(f"{study}_link_tool_geoms_{username}.zip"), media_type='application/octet-stream')
