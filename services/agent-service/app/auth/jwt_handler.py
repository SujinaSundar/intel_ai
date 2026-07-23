"""
JWT token utilities.
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.database.config import settings

# ---------------------------------------------------------------------
# JWT Configuration
# ---------------------------------------------------------------------

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


# ---------------------------------------------------------------------
# Create JWT Token
# ---------------------------------------------------------------------

def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.
    """

    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


# ---------------------------------------------------------------------
# Verify JWT Token
# ---------------------------------------------------------------------

def verify_access_token(token: str) -> dict | None:
    """
    Verify and decode a JWT access token.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return payload

    except JWTError:
        return None