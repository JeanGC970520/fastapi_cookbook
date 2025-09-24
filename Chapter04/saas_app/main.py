from contextlib import (
    asynccontextmanager,
)
from typing import Annotated

import premium_access
import rbac
import security
from db_connection import get_engine, get_session
from fastapi import Depends, FastAPI, HTTPException, status
from models import Base
from operations import add_user
from responses import ResponseCreateUser, UserCreateBody, UserCreateResponse
from sqlalchemy.orm import Session


# Lifespan defines the actions to execute before the app starts up.
# And define the logic that should be executed when app shutting down
# https://fastapi.tiangolo.com/advanced/events/
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Sync DB with our models before app starts up
    Base.metadata.create_all(bind=get_engine())
    yield

app = FastAPI(
    title="SaaS aplication", lifespan=lifespan
)
app.include_router(security.router)
app.include_router(premium_access.router)
app.include_router(rbac.router)


@app.post(
    "/register/user",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseCreateUser,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "The user already exists"
        }
    },
)
def register(
    user: UserCreateBody,
    session: Session = Depends(get_session)
) -> dict[str, UserCreateResponse]:
    user = add_user(
        session=session, **user.model_dump()
    )
    if not user:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "username or email already exists",
        )
    user_response = UserCreateResponse(
        username=user.username, email=user.email
    )
    return {
        "message": "user created",
        "user": user_response,
    }
