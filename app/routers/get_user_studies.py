from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from data_structures import schemas, database, crud
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/get_user_studies/", response_model=schemas.UserStudies)
def user_studies(
        username: str,
        schema: str = Query(...,
                            description="The schema to use (lts or sidewalk)"),
        db: Session = Depends(database.get_db_for_schema)):

    db_studies = crud.get_projects_by_user(db, username)

    if db_studies is None:
        # Handle no studies found
        return JSONResponse(
            status_code=404,
            content={"message": "No studies have been created yet."}
        )

    db_studies_transformed = []
    for item in db_studies:
        study_info = {
            "username": item.username,
            "seg_name": item.seg_name,
            "has_isochrone": item.has_isochrone if item.has_isochrone is not None else False,
            "miles": item.miles if item.miles is not None else 0,
            "total_pop": item.total_pop if item.total_pop is not None else 0,
            "hisp_lat": item.hisp_lat if item.hisp_lat is not None else 0,
            "circuit": item.circuit,
            "total_jobs": item.total_jobs if item.total_jobs is not None else 0,
            "bike_crashes": item.bike_crashes if item.bike_crashes is not None else 0,
            "ped_crashes": item.ped_crashes if item.ped_crashes is not None else 0,
            "essential_services": item.essential_services if item.essential_services is not None else 0,
            "rail_stations": item.rail_stations if item.rail_stations is not None else 0,
            "geom": str(item.geom)
        }
        db_studies_transformed.append(study_info)

    return {"studies": db_studies_transformed}
