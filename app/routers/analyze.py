import os
from typing_extensions import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from dotenv import load_dotenv
from lts_island_connectivity import StudySegment, SegmentNameConflictError

from data_structures import schemas
from . import basic_auth

load_dotenv()
URL_ROOT = os.environ.get("URL_ROOT", "")

router = APIRouter()


@router.post(f"{URL_ROOT}/analyze/", response_model=schemas.AnalyzeResponse)
async def analyze_segment(
    basic_auth: Annotated[str, Depends(basic_auth)],
    data: schemas.AnalyzeRequest,
    overwrite: bool = Query(False, description="Flag to overwrite existing segment"),
):
    if data.connection_type == "bike":
        cx_type = "lts"
    elif data.connection_type == "pedestrian":
        cx_type = "sidewalk"
    else:
        raise HTTPException(
            status_code=422, detail="Connection type must be 'bike' or 'pedestrian'"
        )
    for feature in data.geo_json.features:
        try:
            StudySegment(cx_type, feature.dict(), data.username, overwrite=overwrite)
        except SegmentNameConflictError as exc:
            raise HTTPException(status_code=400, detail=str(exc))

    return {"message": "Segments processed successfully"}
