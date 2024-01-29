import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Query

from data_structures import crud, database
from sqlalchemy.orm import Session

load_dotenv()
URL_ROOT = os.getenv("URL_ROOT")

router = APIRouter()


@router.get(f"{URL_ROOT}/delete/")
def delete(
    username: str,
    seg_name: str,
    schema: str = Query(..., description="The schema to use (lts or sidewalk)"),
    db: Session = Depends(database.get_db_for_schema),
):
    crud.delete_study(db, username, seg_name)

    return {"success": "study deleted successfully"}
