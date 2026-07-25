"""
Authentication schemas.

Pydantic models for user
registration, login,
and JWT authentication.
"""

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


# -----------------------------------------------------
# User Registration
# -----------------------------------------------------

class UserRegisterRequest(BaseModel):
    """
    Request model for user registration.
    """

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the user.",
        examples=["John Doe"],
    )

    email: EmailStr = Field(
        ...,
        description="User email address.",
        examples=["john@example.com"],
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password.",
        examples=["StrongPassword123!"],
    )


# -----------------------------------------------------
# User Login
# -----------------------------------------------------

class UserLoginRequest(BaseModel):
    """
    Request model for user login.
    """

    email: EmailStr = Field(
        ...,
        description="Registered email address.",
        examples=["john@example.com"],
    )

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password.",
    )


# -----------------------------------------------------
# User Response
# -----------------------------------------------------

class UserResponse(BaseModel):
    """
    User information returned by the API.
    """

    id: int

    name: str

    email: EmailStr

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


# -----------------------------------------------------
# JWT Token Response
# -----------------------------------------------------

class TokenResponse(BaseModel):
    """
    JWT authentication response.
    """

    access_token: str = Field(
        ...,
        description="JWT access token.",
    )

    token_type: str = Field(
        default="bearer",
        description="Authentication scheme.",
        examples=["bearer"],
    )