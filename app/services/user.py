from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserAdminUpdate
from app.utils.password import hash_password


def get_users(db: Session):
    users = db.query(User).all()

    return users


def get_user(
    db: Session,
    user_id: int
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    return user


def update_user(
    db: Session,
    user: User,
    user_data: UserAdminUpdate
):
    user.full_name = user_data.full_name
    user.email = user_data.email
    user.role = user_data.role
    user.department_id = user_data.department_id
    user.manager_id = user_data.manager_id
    user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)

    return user


def update_user_password(
    db: Session,
    user: User,
    password: str
):
    hashed_password = hash_password(password)

    user.password_hash = hashed_password

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User
):
    db.delete(user)
    db.commit()

    return True