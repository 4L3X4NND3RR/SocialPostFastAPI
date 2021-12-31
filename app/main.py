from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from starlette.responses import Response

import psycopg2
from psycopg2.extras import RealDictCursor

from app.model.social_post import SocialPost
from app.config import config


app = FastAPI()

try:
    params = config()
    conn = psycopg2.connect(**params, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was succesfull!")
except Exception as error:
    print("Connecting to the database failed.")
    print("Error: ", error)


@app.get("/")
async def root():
    return {"message": "Hakuna Matata!"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM post")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: SocialPost):
    cursor.execute("INSERT INTO post(title, content, published) VALUES(%s, %s, %s) RETURNING *",
                   (new_post.title, new_post.content, new_post.published))
    post = cursor.fetchone()
    conn.commit()
    return {"data": post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM post WHERE id = %s", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not found post with id - {id}")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM post WHERE id = %s RETURNING *", (str(id)))
    deleted = cursor.fetchone()
    conn.commit()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not found post with id - {id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts")
def update_post(update_post: SocialPost):
    cursor.execute("UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
                   (update_post.title, update_post.content, update_post.published, update_post.id))
    updated = cursor.fetchone()
    conn.commit()
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not found post with id - {update_post.id}")
    return {"data": updated}
