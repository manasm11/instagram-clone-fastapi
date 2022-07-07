from fastapi import FastAPI

import exceptions
from db.database import Base, _engine
from routers import user

# Creates Database and Tables
Base.metadata.create_all(_engine)

app = FastAPI()

app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "API is running"}


app.add_exception_handler(exceptions.UserExists, exceptions.user_exists)
