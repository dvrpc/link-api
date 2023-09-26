from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analyze
from data_structures import models
from data_structures.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# tighten this up for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router)


@app.get("/")
async def root():
    return {"message": "More to come soon"}
