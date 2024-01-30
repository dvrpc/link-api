import os
from typing_extensions import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Query

from data_structures import crud, database
from sqlalchemy.orm import Session
from . import basic_auth

load_dotenv()
URL_ROOT = os.environ.get("URL_ROOT", "")

router = APIRouter()


@router.get(f"{URL_ROOT}/delete/")
def delete(
    basic_auth: Annotated[str, Depends(basic_auth)],
    username: str,
    seg_name: str,
    schema: str = Query(..., description="The schema to use (lts or sidewalk)"),
    db: Session = Depends(database.get_db_for_schema),
):
    crud.delete_study(db, username, seg_name)

    return {"success": "study deleted successfully"}
