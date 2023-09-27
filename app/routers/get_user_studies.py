from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


@router.get("/get_user_studies")
def user_studies():

    return {"message": "Here's your data bro"}
