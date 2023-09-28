from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

# This file is where SQLalchemy models live. These directly match DB schema.


class Project(Base):
    __tablename__ = "user_segments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    seg_name = Column(String)
    # geom = Column(Geometry)
