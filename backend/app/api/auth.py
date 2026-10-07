from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)

from app.db.session import get_session
from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserResponse,
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


# ============================================================
# REGISTER
# ============================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_session),
):
    existing_user = db.scalar(
        select(User).where(
            or_(
                User.username == user_data.username,
                User.email == user_data.email,
            )
        )
    )

    if existing_user:

        if existing_user.username == user_data.username:
            raise HTTPException(
                status_code=409,
                detail="Username already exists.",
            )

        raise HTTPException(
            status_code=409,
            detail="Email already exists.",
        )

    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(
            user_data.password
        ),
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


# ============================================================
# LOGIN
# ============================================================

@router.post(
    "/login",
)
def login_user(
    username: str,
    password: str,
    db: Session = Depends(get_session),
):
    user = db.scalar(
        select(User).where(
            or_(
                User.username == username,
                User.email == username,
            )
        )
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username/email or password.",
        )

    password_valid = verify_password(
        password,
        user.password_hash,
    )

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid username/email or password.",
        )

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "username": user.username,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user