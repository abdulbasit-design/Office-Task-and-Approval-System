from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.department import (
    DepartmentCreate,
    DepartmentResponse
)
from app.services.department import (
    create_department,
    get_departments,
    get_department,
    update_department,
    delete_department
)
from app.dependencies.auth import get_current_user, require_role
from app.models.user import User


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post(
    "",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create(
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    department = create_department(
        db,
        department_data
    )

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Department already exists"
        )

    return department


@router.get(
    "",
    response_model=list[DepartmentResponse]
)
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    departments = get_departments(db)

    return departments


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse
)
def get_one(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    department = get_department(
        db,
        department_id
    )

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    return department


@router.put(
    "/{department_id}",
    response_model=DepartmentResponse
)
def update(
    department_id: int,
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    department = get_department(
        db,
        department_id
    )

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    updated_department = update_department(
        db,
        department,
        department_data
    )

    return updated_department


@router.delete(
    "/{department_id}"
)
def delete(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    department = get_department(
        db,
        department_id
    )

    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )

    delete_department(
        db,
        department
    )

    return {
        "message": "Department deleted successfully"
    }