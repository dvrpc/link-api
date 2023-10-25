from fastapi import APIRouter, Depends, Query
from dotenv import load_dotenv
from data_structures import schemas, database, crud, models
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

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
    blobs = crud.get_geoms_by_user_study(db, username, study, models.UserBlobs)
    # buffers = crud.get_geoms_by_user_study(
    #     db, username, study, models.UserBuffers)
    # isochrones = crud.get_geoms_by_user_study(
    #     db, username, study, models.UserIsochrones)
    # study_geoms = [segments, blobs, buffers, isochrones]
    study_geoms = blobs
    if study_geoms is None:
        return JSONResponse(content={"geometries": ["No geometries exist!"]})
    else:
        print(study_geoms)
        # geoms_transformed = [
        #     {"username": item.username,
        #         "segment_geom": item.segments,
        #         "blob_geom": item.blobs,
        #         "isochrone_geom": item.isochrone,
        #         "buffer_geom": item.buffers
        #      } for item in study_geoms]
        geoms_transformed = [study_geoms]
        return {"geometries": geoms_transformed}
