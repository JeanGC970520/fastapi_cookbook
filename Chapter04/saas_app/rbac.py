from typing import Annotated

from db_connection import get_session
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from models import Role
from pydantic import BaseModel, EmailStr
from security import (
    decode_access_token,
    oauth2_scheme,
)
from sqlalchemy.orm import Session


class UserCreateRequestWithRole(BaseModel):
    username: str
    email: EmailStr
    role: Role


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> UserCreateRequestWithRole:
    """Method to search the current User based on its Token

    Args:
        token (str, optional): 
            Bearer token that authorize current User. 
            Defaults to Depends(oauth2_scheme).
        session (Session, optional): 
            Session to interact with our User table.
            Defaults to Depends(get_session).

    Raises:
        HTTPException: Error response by unauthorized User

    Returns:
        UserCreateRequestWithRole: User with role
    """
    user = decode_access_token(token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized",
        )

    return UserCreateRequestWithRole(
        username=user.username,
        email=user.email,
        role=user.role,
    )

def get_premium_user(
    current_user: Annotated[
        get_current_user, Depends()
    ]
):
    """Method to verify a premium User

    Args:
        current_user (Annotated[ get_current_user, Depends): 
            Get current user

    Raises:
        HTTPException: Error when user is not premium (not authorized)

    Returns:
        User: Response about premium User
    """
    if current_user.role != Role.premium:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized",
        )
    return current_user

router = APIRouter()

@router.get(
    "/welcome/all-users",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User not authorized"
        }
    },
)
def all_users_can_access(
    user: Annotated[get_current_user, Depends()]
):
    """Basic endpoint that can access any User

    Args:
        user (Annotated[get_current_user, Depends): 
            An authorized commun User

    Returns:
        Iterable: Success response by authorized User
    """
    return {
        f"Hello {user.username}, "
        "welcome to your space"
    }

@router.get(
    "/welcome/premium-user",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "User not authorized"
        }
    },
)
def only_premium_users_can_access(
    user: UserCreateRequestWithRole = Depends(
        get_premium_user
    ),
):
    """Endpoint that only access premium Users

    Args:
        user (UserCreateRequestWithRole, optional): 
            A premium authorized User.
            Defaults to Depends( get_premium_user ).

    Returns:
        Iterable: Success response by authorized User 
    """
    return {
        f"Hello {user.username}, "
        "Welcome to your premium space"
    }

