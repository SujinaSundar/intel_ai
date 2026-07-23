"""
Authentication service.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status


from app.auth.jwt_handler import create_access_token
from app.auth.password import hash_password, verify_password
from app.database.models import User
from app.schemas.auth import (
    UserLoginRequest,
    UserRegisterRequest,
)


class AuthService:
    """
    Handles user registration and login.
    """

    def __init__(self, db: Session):
        self.db = db

    # ---------------------------------------------------------
    # Register
    # ---------------------------------------------------------

    def register(self, request: UserRegisterRequest):
        print("========== REGISTER ==========")
        print("Request:", request)

        existing_user = (
            self.db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        print("Existing User:", existing_user)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )
        
        user = User(
            name=request.name,
            email=request.email,
            password_hash=hash_password(request.password),
            is_active=True,
        )
        print("Password:", request.password)
        print("Password length:", len(request.password))

        print("Before add")

        self.db.add(user)

        print("Before commit")

        self.db.commit()

        print("After commit")

        self.db.refresh(user)

        print("Created User:", user.id, user.email)

        return user

    # ---------------------------------------------------------
    # Login
    # ---------------------------------------------------------

    def login(self, request: UserLoginRequest):
        print("\n========== LOGIN ==========")
        print("Email:", request.email)
        print("Password:", request.password)

        user = (
            self.db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        print("User Found:", user)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        print("Stored Hash:", user.password_hash)

        password_ok = verify_password(
            request.password,
            user.password_hash,
        )

        print("Password Match:", password_ok)

        if not password_ok:
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

        return {
            "access_token": token,
            "token_type": "bearer",
        }