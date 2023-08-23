from pydantic import BaseModel

# This file is where Pydantic models live. As a note to self, Pydantic is more
# for returning data from the API in a specific format. Doesn't have to include all of
# the SQLAlchemy tables.


class UserBase(BaseModel):
    username: str


class UserInDB(UserBase):
    hashed_password: str


class UserCreate(UserBase):
    """This class inherits from userbase and adds a password"""
    password: str


class User(UserBase):
    """This class is used to return a user that's already in the DB."""
    id: int
    is_active: bool

    class Config:
        from_attributes = True  # this variable was called orm mode previously


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
