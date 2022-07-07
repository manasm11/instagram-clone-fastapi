from fastapi import FastAPI

from db.database import Base, _engine

Base.metadata.create_all(_engine)
from routers import user

app = FastAPI()
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "API is running"}
