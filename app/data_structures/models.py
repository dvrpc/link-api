from sqlalchemy import Boolean, Column, Integer, String, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from geoalchemy2 import Geometry

# This file is where SQLalchemy models live. These directly match DB schema.


class UserSegments(Base):
    __tablename__ = "user_segments"

    id = Column(Integer, ForeignKey('user_segments.id'),
                primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    seg_name = Column(String)
    has_isochrone = Column(Boolean)
    miles = Column(Float)
    total_pop = Column(Integer)
    disabled = Column(Integer)
    ethnic_minority = Column(Integer)
    female = Column(Integer)
    foreign_born = Column(Integer)
    lep = Column(Integer)
    low_income = Column(Integer)
    older_adult = Column(Integer)
    racial_minority = Column(Integer)
    youth = Column(Integer)
    circuit = Column(JSON)
    total_jobs = Column(Integer)
    bike_ped_crashes = Column(JSON)
    essential_services = Column(JSON)
    rail_stations = Column(JSON)
    deleted = Column(Boolean)
    geom = Column(Geometry(geometry_type="LINESTRING", srid=4326))

    user_blobs = relationship(
        "UserBlobs", uselist=False, back_populates="user_segments")
    user_buffers = relationship(
        "UserBuffers", uselist=False, back_populates="user_segments")
    user_isochrones = relationship(
        "UserIsochrones", uselist=False, back_populates="user_segments")


class UserBlobs(Base):
    __tablename__ = "user_blobs"
    id = Column(Integer, ForeignKey('user_segments.id'),
                primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    geom = Column(Geometry(geometry_type='POLYGON', srid=4326))
    user_segments = relationship("UserSegments", back_populates="user_blobs")


class UserBuffers(Base):
    __tablename__ = "user_buffers"
    id = Column(Integer, ForeignKey('user_segments.id'),
                primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    geom = Column(Geometry(geometry_type='POLYGON', srid=4326))
    user_segments = relationship("UserSegments", back_populates="user_buffers")


class UserIsochrones(Base):
    __tablename__ = "user_isochrones"
    id = Column(Integer, ForeignKey('user_segments.id'),
                primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    geom = Column(Geometry(geometry_type='POLYGON', srid=4326))
    user_segments = relationship(
        "UserSegments", back_populates="user_isochrones")
