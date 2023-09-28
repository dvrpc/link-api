from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeMeta

load_dotenv()

DB_URI = os.getenv("DB_URI")


def set_search_path(db, schema):
    db.execute(text(f"SET search_path TO {schema}"))


def after_begin_bike(session, transaction, connection):
    set_search_path(connection, "lts")


def after_begin_ped(session, transaction, connection):
    set_search_path(connection, "sidewalk")


engine_bike = create_engine(DB_URI)
engine_ped = create_engine(DB_URI)

SessionLocalBike = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_bike)
SessionLocalPed = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_ped)

event.listen(SessionLocalBike, "after_begin", after_begin_bike)
event.listen(SessionLocalPed, "after_begin", after_begin_ped)

Base: DeclarativeMeta = declarative_base()


def get_db_for_schema(schema: str):
    if schema == 'lts':
        return SessionLocalBike()
    elif schema == 'sidewalk':
        return SessionLocalPed()
    else:
        raise ValueError("Invalid schema")
