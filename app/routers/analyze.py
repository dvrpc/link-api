from fastapi import Depends,  HTTPException,  APIRouter
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from data_structures import schemas, crud
from data_structures.database import get_db

load_dotenv()

router = APIRouter()


@router.post("/analyze/")
def analyze_segment(geo_json: schemas.GeoJson):
    print(geo_json)
    return {"message": "Data received"}
