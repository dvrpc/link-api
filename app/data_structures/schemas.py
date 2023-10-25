from pydantic import BaseModel, Field
from typing import List, Any


# This file is where Pydantic models live. As a note to self, Pydantic is more
# for returning data from the API in a specific format. Doesn't have to include all of
# the SQLAlchemy tables.

class FeatureModel(BaseModel):
    type: str
    geometry: dict
    properties: dict = Field(..., example={"name": "segment_name"})


class GeoJson(BaseModel):
    type: str
    features: list[FeatureModel]


class AnalyzeRequest(BaseModel):
    """For any requests coming in from the analyze button."""
    connection_type: str
    geo_json: GeoJson
    username: str


class UserStudy(BaseModel):
    username: str
    seg_name: str
    has_isochrone: bool
    miles: float
    total_pop: int
    hisp_lat: int
    circuit: Any
    jobs: Any
    bike_crashes: Any
    ped_crashes: Any
    essential_services: Any
    rail_stations: Any
    geom: str

    @classmethod
    def from_orm(cls, obj):
        geom = obj.geom.to_wkt()
        return cls(**obj.__dict__, geom=geom)


class UserStudies(BaseModel):
    studies: List[UserStudy]


class RenameRequest(BaseModel):
    oldName: str = Field(..., alias='oldName')
    newName: str = Field(..., alias='newName')


class Geom(BaseModel):
    geom: str


class UserGeoms(BaseModel):
    List[Geom]
