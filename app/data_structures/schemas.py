from pydantic import BaseModel, Field
from typing import List


# This file is where Pydantic models live. As a note to self, Pydantic is more
# for returning data from the API in a specific format. Doesn't have to include all of
# the SQLAlchemy tables.


class GeoJson(BaseModel):
    type: str
    features: list


class AnalyzeRequest(BaseModel):
    """For any requests coming in from the analyze button."""
    connection_type: str
    geo_json: GeoJson
    username: str


class UserStudy(BaseModel):
    username: str
    seg_name: str
    has_isochrone: bool


class UserStudies(BaseModel):
    studies: List[UserStudy]


class RenameRequest(BaseModel):
    oldName: str = Field(..., alias='oldName')
    newName: str = Field(..., alias='newName')
