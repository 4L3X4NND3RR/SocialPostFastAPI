from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .config import config
from .database import engine
from .routers import post, user

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

try:
    params = config()
    conn = psycopg2.connect(**params, cursor_factory=RealDictCursor)
    conn.cursor()
    print("Database connection was succesfull!")
except Exception as error:
    print("Connecting to the database failed.")
    print("Error: ", error)


@app.get("/")
async def root():
    return {"message": "Hakuna Matata!"}

app.include_router(post.router)
app.include_router(user.router)
