from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy.orm import Session
from database import SessionLocal, User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

class UserBody(BaseModel):
    """
        Model to manage DATA VALIDATION with Pydantic
    """
    name: str
    email: str

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.post("/user")
def add_new_user(
    user: UserBody,
    db: Session = Depends(get_db)
):
    """
        Path to add new User to de DB, use Pydantic to make data validation.
        Requieres: 
            - user -> User model.
    """
    new_user = User(
        name=user.name,
        email=user.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user")
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
        Method to manage user request with an user id like QUERY PARAM
        Requiere:
            - user_id
    """
    user = (
        db.query(User).filter(
            User.id == user_id,
        ).first()
    )
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user

@app.post("/user/{user_id}") # PATH parameters
def update_user(
    user_id: int,
    user: UserBody,
    db: Session = Depends(get_db),
):
    """
        Method to manage updates in User table, use PATH parameters and Pydantic to validate data
        Requieres:
            - user_id -> Like PATH param
            - user    -> Like body 
    """
    db_user = (
        db.query(User).filter(
            User.id == user_id,
        ).first()
    )
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    db_user.name = user.name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/user")
def delete_user(
    user_id: int, db: Session = Depends(get_db)
):
    """
        Method to delete a single user with User ID, user QUERY params
        Requiere:
            user_id -> Like QUERY param
    """
    db_user = (
        db.query(User).filter(
            User.id == user_id
        ).first()
    )
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}