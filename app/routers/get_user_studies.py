from fastapi import APIRouter, Depends, Query
from dotenv import load_dotenv
from data_structures import schemas, database, crud
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from fastapi.responses import JSONResponse

load_dotenv()

router = APIRouter()


@router.get("/study_exists/")
async def study_exists_endpoint(name: str, username: str, schema: str):
    db: Session = database.get_db_for_schema(schema)
    query = text("SELECT EXISTS (SELECT 1 FROM {}.user_segments WHERE seg_name = :name AND username = :username)".format(
        schema))

    result = db.execute(query, {'name': name, 'username': username}).scalar()
    return {"exists": result}


@ router.get("/get_user_studies/", response_model=schemas.UserStudies)
def user_studies(
        username: str,
        schema: str = Query(...,
                            description="The schema to use (lts or sidewalk)"),
        db: Session = Depends(database.get_db_for_schema)):
    db: Session = database.get_db_for_schema(schema)
    db_studies = crud.get_projects_by_user(db, username)
    if db_studies is None:
        return JSONResponse(content={"studies": ["No studies have been created yet!"]})
    else:
        db_studies_transformed = [
            {"username": item.username,
                "seg_name": item.seg_name,
                "has_isochrone": item.has_isochrone,
                "miles": item.miles,
                "total_pop": item.total_pop,
                "hisp_lat": item.hisp_lat,
                "circuit": item.circuit,
                "total_jobs": item.total_jobs,
                "bike_crashes": item.bike_crashes,
                "ped_crashes": item.ped_crashes,
                "essential_services": item.essential_services,
                "rail_stations": item.rail_stations,
                "geom": str(item.geom)
             } for item in db_studies]
        return {"studies": db_studies_transformed}
