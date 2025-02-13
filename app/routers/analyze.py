import os
from typing_extensions import Annotated
from pathlib import Path
from requests.exceptions import JSONDecodeError
import time
from requests.exceptions import ConnectionError
import psycopg2
import re

from fastapi import APIRouter, Depends, HTTPException, Query
from dotenv import load_dotenv
from lts_island_connectivity import StudySegment, SegmentNameConflictError
from geoalchemy2 import WKTElement
from sqlalchemy.orm import Session

from data_structures import schemas, database, crud
from . import basic_auth

load_dotenv()
URL_ROOT = os.environ.get("URL_ROOT", "")
pg_config_filepath = os.path.join(
    Path(__file__).parent.parent.parent, "database_connections.cfg"
)

router = APIRouter()

# If isochrone flag is hit, delete the incomplete study that was made
def delete_incomplete_study(username, schema, seg_name):
    DB_URI = os.environ.get("DB_URI", "")

    try:
        conn = psycopg2.connect(DB_URI)
    except:
        print("Unable to connect to database")
    
    rows_deleted  = 0

    with conn.cursor() as curs:
        try:
            query = f"""
                DELETE FROM {schema}.user_segments
                WHERE username = '{username}' AND seg_name = '{seg_name}'
            """
            curs.execute(query)
            rows_deleted = curs.rowcount;
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            print(f"Deleted {rows_deleted} incomplete study")


@router.post(f"{URL_ROOT}/analyze", response_model=schemas.AnalyzeResponse)
async def analyze_segment(
    basic_auth: Annotated[str, Depends(basic_auth)],
    data: schemas.AnalyzeRequest,
    overwrite: bool = Query(False, description="Flag to overwrite existing segment"),
    resubmit: bool = Query(False, description="Flag to override isochrone flag, available on resubmit")
):
    if data.connection_type == "bike":
        cx_type = "lts"
    elif data.connection_type == "pedestrian":
        cx_type = "sidewalk"
    else:
        raise HTTPException(
            status_code=422, detail="Connection type must be 'bike' or 'pedestrian'"
        )

    max_retries = 5
    initial_wait_time = 10  # seconds
    for feature in data.geo_json.features:
        attempt = 0
        while attempt < max_retries:
            try:
                StudySegment(
                    cx_type,
                    feature.dict(),
                    data.username,
                    overwrite=overwrite,
                    pg_config_filepath=pg_config_filepath,
                    override_isochrone_flag=resubmit
                )
                break
            except SegmentNameConflictError as exc:
                raise HTTPException(status_code=400, detail=str(exc))
            except RuntimeError as e:
                raise HTTPException(status_code=500, detail=str(e))
            except JSONDecodeError:
                r = "You might have a multiline in your dataset..."
                raise HTTPException(status_code=400, detail=str(r))
            except psycopg2.errors.InternalError_ as e:
                print(f"PostgreSQL Internal Error encountered: {e}")
                print(feature)
                break
            except ConnectionError:
                if attempt >= max_retries - 1:
                    print(f"Maximum retry attempts reached for feature: {feature}")
                    break
                print(
                    f"Encountered a connection error. Retrying in {initial_wait_time * (2 ** attempt)} seconds..."
                )
                time.sleep(initial_wait_time * (2**attempt))
                overwrite = True
                attempt += 1
            except ValueError as exc:
                exc_str = str(exc)
                if "Isochrone flag error" in exc_str:
                    seg_name = exc_str.split('@')[1]
                    # db = database.get_db_for_schema(cx_type)
                    delete_incomplete_study(data.username, cx_type, seg_name)
                    raise HTTPException(status_code=422, detail="Mileage of connected islands exceeds 300")
                else:
                    raise HTTPException(status_code=422, detail=exc_str)

    return {"message": "Segments processed successfully"}
