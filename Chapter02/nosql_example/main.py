from .logging import logger
from .database import user_collection

from bson import ObjectId
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI()


class User(BaseModel):
    name: str
    email: str


class UserResponse(User):
    id: str


@app.get("/users")
def read_users() -> list[User]:
    return [user for user in user_collection.find()]


# Endpoint to create a new user
@app.post("/user")
def create_user(user: User) -> UserResponse:
    """Create a new user in our 'users' Document

    Args:
        user: new user to insert into document db
    """
    result = user_collection.insert_one(
        user.model_dump(exclude_none=True),
    )
    user_data = user.model_dump()
    logger.debug("{0} user inserted into DB.".format(user_data))
    user_response = UserResponse(
        id=str(result.inserted_id),
        **user.model_dump(),  # Unpacking python dict
    )
    return user_response


# Endpoint to retrieve an existing User
@app.get("/user")
def get_user(user_id: str) -> UserResponse:
    db_user = user_collection.find_one(
        {"_id": ObjectId(user_id) if ObjectId.is_valid(user_id) else None},
    )
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    user_response = UserResponse(
        id=str(db_user["_id"]),
        **db_user,
    )
    return user_response
