from pydantic import BaseModel, Field
from typing import List, Any, Optional, Literal
from enum import Enum


# This file is where Pydantic models live. As a note to self, Pydantic is more
# for returning data from the API in a specific format. Doesn't have to include all of
# the SQLAlchemy tables.
class GeometryType(str, Enum):
    Feature = "Feature"
    Polygon = "Polygon"
    Linetring = "LineString"
    Multilinestring = "MultiLineString"
    Multipolygon = "MultiPolygon"


class Geometry(BaseModel):
    type: GeometryType
    coordinates: List[Any]


class FeatureModel(BaseModel):
    type: str = 'Feature'
    geometry: Optional[Geometry] = None
    properties: Optional[dict] = None
    id: Optional[str] = None


class GeoJson(BaseModel):
    type: str
    features: List[FeatureModel]


class UserStudy(BaseModel):
    username: str
    seg_name: str
    has_isochrone: bool
    miles: float
    total_pop: int
    hisp_lat: int
    circuit: Any
    total_jobs: Any
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
    buffers: Optional[FeatureModel] = None
    isochrones: Optional[FeatureModel] = None
    blobs: Optional[FeatureModel] = None


class UserSegments(BaseModel):
    segments: Optional[FeatureModel] = None


class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: List[FeatureModel]


class AnalyzeRequest(BaseModel):
    """For any requests coming in from the analyze button."""
    connection_type: str
    geo_json: FeatureCollection
    username: str


class AnalyzeResponse(BaseModel):
    message: str
