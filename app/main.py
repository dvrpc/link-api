from fastapi import FastAPI

from routers import authentication

app = FastAPI()


app.include_router(authentication.router)


@app.get("/")
async def root():
    return {"message": "More to come soon"}
