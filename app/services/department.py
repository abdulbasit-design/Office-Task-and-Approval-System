from sqlalchemy.orm import Session

from app.models.department import Department
from app.schemas.department import DepartmentCreate


def create_department(
    db: Session,
    department_data: DepartmentCreate
):
    existing_department = db.query(Department).filter(
        Department.name == department_data.name
    ).first()

    if existing_department:
        return None

    new_department = Department(
        name=department_data.name,
        description=department_data.description
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department


def get_departments(db: Session):
    departments = db.query(Department).all()

    return departments


def get_department(
    db: Session,
    department_id: int
):
    department = db.query(Department).filter(
        Department.id == department_id
    ).first()

    return department


def update_department(
    db: Session,
    department: Department,
    department_data: DepartmentCreate
):
    department.name = department_data.name
    department.description = department_data.description

    db.commit()
    db.refresh(department)

    return department


def delete_department(
    db: Session,
    department: Department
):
    db.delete(department)
    db.commit()

    return True