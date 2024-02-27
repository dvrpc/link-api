import os
from typing_extensions import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from data_structures import database, crud
from . import basic_auth

load_dotenv()
URL_ROOT = os.environ.get("URL_ROOT", "")

router = APIRouter()


@router.get(f"{URL_ROOT}/share")
def share(
    basic_auth: Annotated[str, Depends(basic_auth)],
    username: str,
    seg_name: str,
    shared: bool,
    schema: str = Query(..., description="The schema to use (lts or sidewalk)"),
    db: Session = Depends(database.get_db_for_schema),
):
    crud.share_study(db, username, seg_name, shared)

    return {"success": "share status updated successfully"}
