from fastapi import APIRouter, Query, Depends
from dotenv import load_dotenv
from data_structures import schemas, database, crud
from sqlalchemy.orm import Session


load_dotenv()

router = APIRouter()


@router.post("/rename/")
def analyze_segment(
    data: schemas.RenameRequest,
    username: str = Query(..., description="the user who is renaming"),
    schema: str = Query(..., description="The schema to use (lts or sidewalk)"),
    db: Session = Depends(database.get_db_for_schema),
):
    db_studies = crud.rename_segment(db, data.oldName, data.newName, username)

    return {"message": f"Data received: {db_studies}"}
