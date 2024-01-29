import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeMeta

load_dotenv()

DB_URI = os.getenv("DB_URI")
URL_ROOT = os.getenv("URL_ROOT")


def set_search_path(db, schema):
    db.execute(text(f"SET search_path TO {schema}, public"))


def after_begin_bike(session, transaction, connection):
    set_search_path(connection, "lts")


def after_begin_ped(session, transaction, connection):
    set_search_path(connection, "sidewalk")


engine_bike = create_engine(DB_URI)
engine_ped = create_engine(DB_URI)

SessionLocalBike = sessionmaker(autocommit=False, autoflush=False, bind=engine_bike)
SessionLocalPed = sessionmaker(autocommit=False, autoflush=False, bind=engine_ped)

event.listen(SessionLocalBike, "after_begin", after_begin_bike)
event.listen(SessionLocalPed, "after_begin", after_begin_ped)

Base: DeclarativeMeta = declarative_base()


def get_db_for_schema(schema: str):
    if schema == "lts":
        db = SessionLocalBike()
    elif schema == "sidewalk":
        db = SessionLocalPed()
    else:
        raise ValueError("Invalid schema")
    try:
        yield db
    finally:
        db.close()
