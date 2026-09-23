from fastapi import FastAPI

from app.database import Base, engine
from app.models.department import Department
from app.models.user import User
from app.routes.auth import router as auth_router
from app.routes.department import router as department_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(department_router)


@app.get("/")
def test_connection():
    return {"message": "Database connected successfully"}