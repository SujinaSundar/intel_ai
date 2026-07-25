"""
JWT token utilities.

Provides helper functions
for creating and verifying
JSON Web Tokens (JWT).
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from app.database.config import settings

logger = logging.getLogger(__name__)

# -----------------------------------------------------
# JWT Configuration
# -----------------------------------------------------

SECRET_KEY = settings.JWT_SECRET_KEY

ALGORITHM = settings.JWT_ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES = (
    settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
)


# -----------------------------------------------------
# Create JWT Token
# -----------------------------------------------------


def create_access_token(
    data: dict[str, Any],
) -> str:
    """
    Create a JWT access token.

    Parameters
    ----------
    data : dict[str, Any]
        Payload to include
        in the JWT.

    Returns
    -------
    str
        Encoded JWT token.
    """

    payload = data.copy()

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload.update(
        {
            "exp": expire,
        }
    )

    logger.debug(
        "Creating JWT token."
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# -----------------------------------------------------
# Verify JWT Token
# -----------------------------------------------------


def verify_access_token(
    token: str,
) -> dict[str, Any] | None:
    """
    Verify and decode
    a JWT access token.

    Parameters
    ----------
    token : str
        JWT token.

    Returns
    -------
    dict[str, Any] | None
        Decoded payload if
        valid, otherwise None.
    """

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        if not payload.get("sub"):

            logger.warning(
                "JWT token missing subject."
            )

            return None

        return payload

    except JWTError:

        logger.warning(
            "JWT verification failed."
        )

        return None