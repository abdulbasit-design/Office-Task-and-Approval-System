from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskSubmit,
    TaskReject,
    TaskResponse
)
from app.services.task import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    submit_task,
    approve_task,
    reject_task
)
from app.dependencies.auth import get_current_user, require_role


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("manager")
    )
):
    task = create_task(
        db,
        task_data,
        current_user
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned user not found"
        )

    return task


@router.get(
    "",
    response_model=list[TaskResponse]
)
def get_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = get_tasks(
        db,
        current_user
    )

    return tasks


@router.get(
    "/{task_id}",
    response_model=TaskResponse
)
def get_one(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = get_task(
        db,
        task_id,
        current_user
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse
)
def update(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("manager")
    )
):
    task = get_task(
        db,
        task_id,
        current_user
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    updated_task = update_task(
        db,
        task,
        task_data,
        current_user
    )

    if updated_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned user not found"
        )

    return updated_task


@router.post(
    "/{task_id}/submit",
    response_model=TaskResponse
)
def submit(
    task_id: int,
    task_data: TaskSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("employee")
    )
):
    task = get_task(
        db,
        task_id,
        current_user
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    submitted_task = submit_task(
        db,
        task,
        task_data,
        current_user
    )

    if submitted_task is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task cannot be submitted in its current status"
        )

    return submitted_task


@router.post(
    "/{task_id}/approve",
    response_model=TaskResponse
)
def approve(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("manager")
    )
):
    task = get_task(
        db,
        task_id,
        current_user
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.status != "SUBMITTED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only submitted tasks can be approved"
        )

    approved_task = approve_task(
        db,
        task,
        current_user
    )

    if approved_task is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only submitted tasks can be approved"
        )

    return approved_task


@router.post(
    "/{task_id}/reject",
    response_model=TaskResponse
)
def reject(
    task_id: int,
    task_data: TaskReject,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("manager")
    )
):
    task = get_task(
        db,
        task_id,
        current_user
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if task.status != "SUBMITTED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only submitted tasks can be rejected"
        )

    rejected_task = reject_task(
        db,
        task,
        task_data,
        current_user
    )

    if rejected_task is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only submitted tasks can be rejected"
        )

    return rejected_task

