from .logging import logger
from .database import user_collection

from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from fastapi import FastAPI, HTTPException

app = FastAPI()


# Manage complex data types
class Tweet(BaseModel):
    content: str
    hashtags: list[str]


class User(BaseModel):
    name: str
    email: EmailStr
    age: int
    tweets: list[Tweet] | None = None

    # Add Custom Validator
    @field_validator("age")
    def validate_age(cls, value):
        if value < 18 or value > 100:
            raise ValueError(
                "Age must be between 18 and 100",
            )
        return value


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
    db_user["id"] = str(db_user["_id"])
    return db_user
