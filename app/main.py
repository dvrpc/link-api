from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analyze, get_user_studies, rename


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


@app.get("/")
async def root():
    return {"message": "More to come soon"}
