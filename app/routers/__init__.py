import os
from typing_extensions import Annotated

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

load_dotenv()
USERNAME = os.environ.get("BASIC_AUTH_USERNAME")
PASSWORD = os.environ.get("BASIC_AUTH_PASSWORD")

security = HTTPBasic()


def basic_auth(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """
    Create a simple verification method using Basic HTTP Authentication.
    In any HTTP request, use the Basic Auth Authorization header to provide a username & password,
    which will be validated against the environment variables in the .env file.
    This fn can be used in an endpoint to add authentication to it.
    """
    is_correct_username = secrets.compare_digest(
        credentials.username.encode("utf8"), USERNAME.encode("utf8")
    )
    is_correct_password = secrets.compare_digest(
        credentials.password.encode("utf8"), PASSWORD.encode("utf8")
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return
