from fastapi import FastAPI

from app.database import Base, engine
from app.models.department import Department
from app.models.user import User
from app.models.task import Task

from app.routes.auth import router as auth_router
from app.routes.department import router as department_router
from app.routes.user import router as user_router
from app.routes.task import router as task_router


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(auth_router)
app.include_router(department_router)
app.include_router(user_router)
app.include_router(task_router)


@app.get("/")
def test_connection():
    return {
        "message": "Database connected successfully"
    }