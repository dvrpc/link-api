from fastapi import APIRouter
from dotenv import load_dotenv
from data_structures import schemas

load_dotenv()

router = APIRouter()


@router.post("/analyze/")
def analyze_segment(data: schemas.AnalyzeRequest):
    print(data)
    return {"message": "Data received"}
