from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

# This file is where SQLalchemy models live. These directly match DB schema.


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
