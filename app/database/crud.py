from typing import Optional
from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, id: int) -> Optional[models.User]:

    return db.query(models.User).filter(models.User.id == id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:

    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session) -> Optional[models.User]:

    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:

    db_user = models.User(email=user.email, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.UserUpdate, id: int) -> Optional[models.User]:

    db_user = get_user(db, id)
    if db_user is None:
        return None
    db_user.name = user.name if user.name is not None else db_user.name
    db_user.email = user.email if user.email is not None else db_user.email
    db.commit()
    return db_user


def delete_user(db: Session, id: int) -> bool:

    db_user = get_user(db, id)
    if db_user is None:
        return False
    db.delete(db_user)
    db.commit()
    return True


def get_comment(db: Session, id: int) -> Optional[models.Comment]:

    return db.query(models.Comment).filter(models.Comment.id == id).first()


def get_comments(db: Session) -> Optional[models.User]:

    return db.query(models.Comment).all()


def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int) -> models.Comment:

    db_comment = models.Comment(text=comment.text, owner_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update_comment(db: Session, comment: schemas.CommentUpdate, id: int) -> Optional[models.Comment]:

    db_comment = get_comment(db, id)
    if db_comment is None:
        return None
    db_comment.text = comment.text
    db.commit()
    return db_comment


def delete_comment(db: Session, id: int) -> bool:

    db_comment = get_comment(db, id)
    if db_comment is None:
        return False
    db.delete(db_comment)
    db.commit()
    return True
