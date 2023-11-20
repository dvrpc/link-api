from fastapi import Response, APIRouter, Depends
from data_structures import database
from sqlalchemy.sql import text
from sqlalchemy.orm import Session
import csv
import io

router = APIRouter()


@router.get("/get-csv/")
def get_csv(response: Response, schema: str,  username: str, db: Session = Depends(database.get_db_for_schema)):
    query = text(f"SELECT * FROM {schema}.user_segments")

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
