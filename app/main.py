from routers import authentication
from fastapi import FastAPI
from routers import users
from data_structures import models
from data_structures.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(users.router)
app.include_router(authentication.router)


@app.get("/")
async def root():
    return {"message": "More to come soon"}
