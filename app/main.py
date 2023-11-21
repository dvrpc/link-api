from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analyze, get_user_studies, rename, get_user_geoms, get_csv, get_user_segment


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
app.include_router(get_user_studies.router)
app.include_router(rename.router)
app.include_router(get_user_geoms.router)
app.include_router(get_csv.router)
app.include_router(get_user_segment.router)


@app.get("/")
async def root():
    return {"message": "Go to /docs!"}
