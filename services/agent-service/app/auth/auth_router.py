"""
Authentication API routes.
"""

import logging

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.auth_service import AuthService
from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.database.models import User
from app.schemas.auth import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# -----------------------------------------------------
# Register
# -----------------------------------------------------


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(
    request: UserRegisterRequest,
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Register a new user.
    """

    logger.info(
        "User registration requested for email=%s",
        request.email,
    )

    service = AuthService(db)

    return service.register(request)


# -----------------------------------------------------
# Login
# -----------------------------------------------------


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Authenticate a user and
    return an access token.
    """

    logger.info(
        "Login requested for email=%s",
        form_data.username,
    )

    request = UserLoginRequest(
        email=form_data.username,
        password=form_data.password,
    )

    service = AuthService(db)

    return service.login(request)


# -----------------------------------------------------
# Current User
# -----------------------------------------------------


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
)
def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Return the currently
    authenticated user.
    """

    logger.info(
        "Fetching profile for user=%s",
        current_user.email,
    )

    return current_user