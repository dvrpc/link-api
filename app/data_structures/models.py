from sqlalchemy import Boolean, Column, Integer, String, Float, JSON
from .database import Base

# This file is where SQLalchemy models live. These directly match DB schema.


class Project(Base):
    __tablename__ = "user_segments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    seg_name = Column(String)
    has_isochrone = Column(Boolean)
    miles = Column(Float)
    total_pop = Column(Integer)
    hisp_lat = Column(Integer)
    circuit = Column(JSON)
    jobs = Column(JSON)
    bike_crashes = Column(JSON)
    ped_crashes = Column(JSON)
    essential_services = Column(JSON)
    rail_stations = Column(JSON)
    geom = Column(Geometry)


class UserBlobs(Base):
    __tablename__ = "user_blobs"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
