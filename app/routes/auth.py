from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth import signup_user, login_user
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.utils.jwt import decode_access_token, create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = signup_user(db, user_data)

    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered"
        )

    return new_user


@router.post("/login")
def login(
    user_data: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
):
    result = login_user(db, user_data)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        max_age=7 * 24 * 60 * 60
    )

    return {
        "access_token": result["access_token"],
        "token_type": result["token_type"]
    }


@router.post("/refresh")
def refresh_token(
    refresh_token: str = Cookie(...)
):
    payload = decode_access_token(refresh_token)

    user_id = int(payload["sub"])

    access_token = create_access_token(user_id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="refresh_token"
    )

    return {
        "message": "Logged out successfully"
    }

@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user 