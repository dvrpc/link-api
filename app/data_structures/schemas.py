from pydantic import BaseModel


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


class UserStudies(BaseModel):
    """For requesting all studies that belong to a user"""
    username: str
