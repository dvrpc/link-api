from fastapi import APIRouter, Depends, Query
from data_structures import database, crud
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/delete/")
def delete(
        username: str,
        seg_name: str,
        schema: str = Query(...,
                            description="The schema to use (lts or sidewalk)"),
        db: Session = Depends(database.get_db_for_schema)):

    crud.delete_study(db, username, seg_name)

    return {"success": "study deleted successfully"}
