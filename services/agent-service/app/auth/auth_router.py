"""
Authentication API routes.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.database.models import User
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.auth_service import AuthService
from app.database.connection import get_db
from app.schemas.auth import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    request: UserRegisterRequest,
    db: Session = Depends(get_db),
):
    """
    Register a new user.
    """
    service = AuthService(db)
    return service.register(request)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    request = UserLoginRequest(
        email=form_data.username,
        password=form_data.password,
    )

    service = AuthService(db)
    return service.login(request)
@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Get details of the currently authenticated user.
    """
    return current_user