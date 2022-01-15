from fastapi import Depends, status, APIRouter
from fastapi.exceptions import HTTPException
from starlette.responses import Response
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.PostTable).all()
    return {"data": posts}


@router.post("", status_code=status.HTTP_201_CREATED)
def create_post(post: models.Post, db: Session = Depends(get_db)):
    new_post = models.PostTable(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.PostTable).filter(models.PostTable.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found post with id - {id}",
        )
    return {"data": post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.PostTable).filter(models.PostTable.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found post with id - {id}",
        )

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("")
def update_post(update_post: models.Post, db: Session = Depends(get_db)):
    post = db.query(models.PostTable).filter(models.PostTable.id == update_post.id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found post with id - {update_post.id}",
        )
    post.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": post.first()}
