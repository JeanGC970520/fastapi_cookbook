from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "hashedsecret",
    },
    "janedoe": {
        "username": "janedoe",
        "hashed_password": "hashedsecret2",
    },
}


# fake functin that hashes password
def fakely_hash_password(password: str):
    return f"hashed{password}"


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# fake token gen
def fake_token_generator(user: UserInDB) -> str:
    return f"tokenized{user.username}"


# fake token resolevet, this doesn't provide any security at all
def fake_token_resolver(
    token: str
) -> UserInDB | None:
    if token.startswith("tokenized"):
        user_id = token.removeprefix("tokenized")
        user = get_user(fake_users_db, user_id)
        return user


# function to retrive a User from the token, use dependency injection
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_from_token(
    token: str = Depends(oauth2_scheme),
) -> UserInDB:
    user = fake_token_resolver(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                "Invalid authentication credentials"
            ),
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user
