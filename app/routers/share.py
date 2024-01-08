from fastapi import APIRouter, Depends, Query
from data_structures import database, crud
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/share/")
def share(
        username: str,
        seg_name: str,
        shared: bool,
        schema: str = Query(...,
                            description="The schema to use (lts or sidewalk)"),
        db: Session = Depends(database.get_db_for_schema)):

    crud.share_study(db, username, seg_name, shared)

    return {"success": "share status updated successfully"}
