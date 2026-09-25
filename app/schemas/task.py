from pydantic import BaseModel
from datetime import datetime


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    assigned_to: int
    deadline: datetime
    priority: str


class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    assigned_to: int
    deadline: datetime
    priority: str


class TaskSubmit(BaseModel):
    submission_note: str | None = None


class TaskReject(BaseModel):
    rejection_reason: str


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    created_by: int
    assigned_to: int
    deadline: datetime
    priority: str
    status: str
    submitted_at: datetime | None
    submission_note: str | None
    approved_at: datetime | None
    approved_by: int | None
    rejection_reason: str | None
    activity_log: list
    created_at: datetime

    model_config = {
        "from_attributes": True
    }