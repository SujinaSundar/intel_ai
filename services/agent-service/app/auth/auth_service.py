"""
Authentication service.
"""

import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.auth.jwt_handler import create_access_token
from app.auth.password import hash_password, verify_password
from app.database.models import User
from app.schemas.auth import (
    UserLoginRequest,
    UserRegisterRequest,
)

logger = logging.getLogger(__name__)


class AuthService:
    """
    Handles user registration
    and authentication.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        """
        Initialize authentication service.
        """

        self.db = db

    # ---------------------------------------------------------
    # Register
    # ---------------------------------------------------------

    def register(
        self,
        request: UserRegisterRequest,
    ) -> User:
        """
        Register a new user.
        """

        logger.info(
            "Register request received for email=%s",
            request.email,
        )

        existing_user = (
            self.db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if existing_user:

            logger.warning(
                "Registration failed. Email already exists: %s",
                request.email,
            )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )

        user = User(
            name=request.name,
            email=request.email,
            password_hash=hash_password(
                request.password
            ),
            is_active=True,
        )

        try:

            self.db.add(user)

            self.db.commit()

            self.db.refresh(user)

            logger.info(
                "User registered successfully. user_id=%s",
                user.id,
            )

            return user

        except SQLAlchemyError:

            self.db.rollback()

            logger.exception(
                "Database error while registering user."
            )

            raise

    # ---------------------------------------------------------
    # Login
    # ---------------------------------------------------------

    def login(
        self,
        request: UserLoginRequest,
    ) -> dict[str, str]:
        """
        Authenticate user and
        generate JWT token.
        """

        logger.info(
            "Login request received for email=%s",
            request.email,
        )

        user = (
            self.db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if (
            not user
            or not verify_password(
                request.password,
                user.password_hash,
            )
        ):

            logger.warning(
                "Invalid login attempt for email=%s",
                request.email,
            )

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        token = create_access_token(
            {
                "sub": user.email,
                "user_id": user.id,
            }
        )

        logger.info(
            "User logged in successfully. user_id=%s",
            user.id,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }