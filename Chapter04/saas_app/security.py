from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from models import User
from jose import jwt, JWTError

from operations import pwd_context, get_user


def authenticate_user(
    session: Session,
    username_or_email: str,
    password: str,
) -> User | None:
    """Function to validate the input bases on either
    the username or email

    Args:
        session (Session): session to connect with our DB
        username_or_email (str): username or email input
        password (str): password input

    Returns:
        User | None: Return a User if the username_or_email
                    and the password are valid.
    """
    user = get_user(session, username_or_email)
    if not user or not pwd_context.verify(
        password,
        user.hashed_password
    ):
        return
    return user


SECRET_KEY = "a_very_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    """Generates JWT access token

    Args:
        data (dict): _description_

    Returns:
        str: JWT token generated
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def decode_access_token(
    token: str, session: Session
) -> User | None:
    """Decode JWT token and verify its valid

    Args:
        token (str): JWT token
        session (Session): session to connect with our DB

    Returns:
        User | None: Valid User or None
    """
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: str = payload.get("sub")
    except JWTError:
        return
    if not username:
        return
    user = get_user(session, username)
    return user
