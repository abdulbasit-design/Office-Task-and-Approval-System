from pydantic import BaseModel
from datetime import datetime


class DepartmentCreate(BaseModel):
    name: str
    description: str | None = None


class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }