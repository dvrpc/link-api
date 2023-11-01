from fastapi import APIRouter
from dotenv import load_dotenv
from data_structures import schemas
from lts_island_connectivity import StudySegment

load_dotenv()

router = APIRouter()


@router.post("/analyze/")
def analyze_segment(data: schemas.AnalyzeRequest):
    if data.connection_type == 'bike':
        cx_type = "lts"
    elif data.connection_type == "pedestrian":
        cx_type = "sidewalk"
    else:
        raise ValueError("connection type must be bike or pedestrian")

    for feature in data.geo_json.features:
        StudySegment(cx_type, feature.dict(), data.username)

    return {"message": "Data received"}
