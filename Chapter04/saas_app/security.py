from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from models import User
from jose import jwt, JWTError
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import (
    OAuth2PasswordRequestForm,
    OAuth2PasswordBearer
)
from pydantic import BaseModel

from operations import pwd_context, get_user
from db_connection import get_session


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
        data (dict): Username information

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


router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post(
    "/token",
    response_model=Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Incorrect username or password"
        }
    },
)
def get_user_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    """Endpoint to get JWT token bases in User credentials

    Args:
        form_data (OAuth2PasswordRequestForm, optional):
            _description_.
            Defaults to Depends().
        session (Session, optional):
            Session to interact with our User table.
            Defaults to Depends(get_session).

    Raises:
        HTTPException: Return UNAUTHORIZED error if username or
        password its invalid

    Returns:
        dict: Access token and its type(Bearer)
    """
    user = authenticate_user(
        session,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get(
    "/users/me",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User not authorized"
        },
        status.HTTP_200_OK: {
            "description": "username authorized"
        },
    },
)
def read_user_me(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
):
    """Valid if the token corresponds with a User

    Args:
        token (str, optional):
            JWT User token. Defaults to Depends(oauth2_scheme).
        session (Session, optional):
            Session to connect with User table.
            Defaults to Depends(get_session).

    Raises:
        HTTPException: 401 UNAUTHORIZED error
        if user doesn't exists

    Returns:
        dict: Authorized information
    """
    user = decode_access_token(token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized",
        )
    return {
        "description": f"{user.username} authorized"
    }
