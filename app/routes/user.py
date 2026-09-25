from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserAdminUpdate, UserResponse
from app.services.user import (
    get_users,
    get_user,
    update_user,
    update_user_password,
    delete_user
)
from app.dependencies.auth import require_role
from app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "",
    response_model=list[UserResponse]
)
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    users = get_users(db)

    return users


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_one(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    user = get_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update(
    user_id: int,
    user_data: UserAdminUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    user = get_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    updated_user = update_user(
        db,
        user,
        user_data
    )

    return updated_user


@router.delete(
    "/{user_id}"
)
def delete(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    user = get_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    delete_user(
        db,
        user
    )

    return {
        "message": "User deleted successfully"
    }