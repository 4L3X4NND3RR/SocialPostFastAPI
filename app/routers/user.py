from fastapi import Depends, status, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from .. import models, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: models.User, db: Session = Depends(get_db)):
    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = models.UserTable(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"data": new_user}


@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserTable).filter(models.UserTable.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found user with id - {id}",
        )
    return {"data": user}
