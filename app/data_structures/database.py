from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

dbschema = 'connect_users,lts,sidewalk,public'
DB_URI = os.getenv("DB_URI")

SQLALCHEMY_DATABASE_URL = DB_URI

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'options': '-csearch_path={}'.format(dbschema)}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()
