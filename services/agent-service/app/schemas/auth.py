"""
Authentication Schemas.

Pydantic models for
user registration,
login, and JWT responses.
"""

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)


# -----------------------------------------------------
# Register
# -----------------------------------------------------

class UserRegisterRequest(BaseModel):
    """
    User registration request.
    """

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )


# -----------------------------------------------------
# Login
# -----------------------------------------------------

class UserLoginRequest(BaseModel):
    """
    User login request.
    """

    email: EmailStr

    password: str


# -----------------------------------------------------
# Response
# -----------------------------------------------------

class UserResponse(BaseModel):
    """
    User information.
    """

    id: int

    name: str

    email: EmailStr

    is_active: bool

    class Config:
        from_attributes = True


# -----------------------------------------------------
# JWT Token
# -----------------------------------------------------

class TokenResponse(BaseModel):
    """
    JWT response.
    """

    access_token: str

    token_type: str = "bearer"