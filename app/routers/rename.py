import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from data_structures import crud, database, schemas

load_dotenv()
URL_ROOT = os.getenv("URL_ROOT")

router = APIRouter()


@router.post(f"{URL_ROOT}/rename/")
def analyze_segment(
    data: schemas.RenameRequest,
    username: str = Query(..., description="the user who is renaming"),
    schema: str = Query(..., description="The schema to use (lts or sidewalk)"),
    db: Session = Depends(database.get_db_for_schema),
):
    db_studies = crud.rename_segment(db, data.oldName, data.newName, username)

    return {"message": f"Data received: {db_studies}"}
