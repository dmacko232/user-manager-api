from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import requests

from .database import crud, models, schemas
from .database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.put("/users/{id}", response_model=schemas.User)
def update_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):

    updated = crud.update_user(db=db, user=user, id=id)
    if updated is None:
        raise HTTPException(status_code=400, detail="User to update not found")
    return updated


@app.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):

    if not crud.delete_user(db=db, id=id):
        raise HTTPException(status_code=400, detail="User to delete not found")
    return {"ok": True}


@app.get("/users", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):

    return crud.get_users(db)


@app.get("/users/{id}", response_model=schemas.User)
def read_user(id: int, db: Session = Depends(get_db)):

    db_user = crud.get_user(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/comments", response_model=schemas.Comment)
def create_comment(user_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):

    if crud.get_user(db, user_id) is None:
        raise HTTPException(status_code=404, detail="User to create comment for not found")
    return crud.create_comment(db=db, comment=comment, user_id=user_id)


@app.put("/comments/{id}", response_model=schemas.Comment)
def update_comment(id: int, user: schemas.CommentUpdate, db: Session = Depends(get_db)):

    updated = crud.update_comment(db=db, user=user, id=id)
    if updated is None:
        raise HTTPException(status_code=400, detail="Comment to update not found")
    return updated


@app.delete("/comments/{id}")
def delete_comment(id: int, db: Session = Depends(get_db)):

    if not crud.delete_comment(db=db, id=id):
        raise HTTPException(status_code=400, detail="Comment to delete not found")
    return {"ok": True}


@app.get("/comments", response_model=List[schemas.Comment])
def read_comments( db: Session = Depends(get_db)):

    return crud.get_comments(db)


@app.get("/comments/{id}", response_model=schemas.Comment)
def read_comment(id: int, db: Session = Depends(get_db)):

    db_user = crud.get_comment(db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_user


@app.get("/animal", response_model=schemas.Animal)
def read_animal():

    r = requests.get("https://zoo-animal-api.herokuapp.com/animals/rand")
    r.raise_for_status()
    data = r.json()
    return schemas.Animal(name=data["name"], latin_name=data["latin_name"])
