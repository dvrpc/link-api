import os
from typing_extensions import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    analyze,
    get_user_studies,
    rename,
    get_user_geoms,
    get_csv,
    get_user_segment,
    delete_flag,
    share,
    basic_auth,
)

load_dotenv()
URL_ROOT = os.environ.get("URL_ROOT", "")

app = FastAPI(docs_url=f"{URL_ROOT}/docs", openapi_url=f"{URL_ROOT}/openapi.json")

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
app.include_router(delete_flag.router)
app.include_router(share.router)


@app.get(f"{URL_ROOT}/")
async def root(basic_auth: Annotated[str, Depends(basic_auth)]):
    return {"message": "Go to /docs!"}
