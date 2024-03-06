import csv
import io
import os
from typing_extensions import Annotated

from dotenv import load_dotenv
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Response

from data_structures import database
from . import basic_auth

load_dotenv()
URL_ROOT = os.environ.get("URL_ROOT", "")

router = APIRouter()


@router.get(f"{URL_ROOT}/get-csv")
def get_csv(
    basic_auth: Annotated[str, Depends(basic_auth)],
    response: Response,
    schema: str,
    username: str,
    db: Session = Depends(database.get_db_for_schema),
):
    query = text(
        f"SELECT * FROM {schema}.user_segments where username = {username} and deleted is not true"
    )

    result = db.execute(query)

    response.headers["Content-Type"] = "text/csv"
    filename = f"{username}_connect_data.csv"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"

    output = io.StringIO()
    writer = csv.writer(output)

    header = result.keys()
    writer.writerow(header)

    for row in result.fetchall():
        writer.writerow(row)

    csv_content = output.getvalue()
    output.close()

    return Response(content=csv_content, media_type="text/csv")
