from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from models import Role
from operations import add_user
from db_connection import get_session
from responses import (
    ResponseCreateUser,
    UserCreateBody,
    UserCreateResponse,
)

router = APIRouter()

@router.post(
    "/register/premium-user",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCreateUser,
    responses={
        status.HTTP_409_CONFLICT : {
            "description": "The user already exists"
        },
        status.HTTP_201_CREATED : {
            "description": "User created"
        }
    }
)
def register_premium_user(
    user: UserCreateBody,
    session: Session = Depends(get_session),
):
    """Endpoint to register a new premium User

    Args:
        user (UserCreateBody): Model to manage a requiered fields about User
        session (Session, optional): 
            Session to interact with our User table. 
            Defaults to Depends(get_session).

    Raises:
        HTTPException: Error if a user is not created

    Returns:
        dict: Successful response about User created
    """
    user = add_user(
        session=session,
        **user.model_dump(),
        role=Role.premium,
    )
    if not user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "username or email already exists"
        )
    user_response = UserCreateResponse(
        username=user.username,
        email=user.email,
    )
    return {
        "message": "user_created",
        "user": user_response
    }