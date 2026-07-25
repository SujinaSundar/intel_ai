"""
Authentication dependencies.

Provides reusable FastAPI
dependencies for JWT
authentication.
"""

import logging

from fastapi import (
    Depends,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from jose import (
    JWTError,
    jwt,
)
from sqlalchemy.orm import Session

from app.database.config import settings
from app.database.connection import get_db
from app.database.models import User

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Retrieve the currently
    authenticated user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
    )

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[
                settings.JWT_ALGORITHM
            ],
        )

        email = payload.get("sub")

        if not email:

            logger.warning(
                "JWT token missing subject."
            )

            raise credentials_exception

    except JWTError:

        logger.warning(
            "Invalid JWT token received."
        )

        raise credentials_exception

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:

        logger.warning(
            "User not found for email=%s",
            email,
        )

        raise credentials_exception

    if not user.is_active:

        logger.warning(
            "Inactive user attempted authentication: %s",
            email,
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive.",
        )

    return user