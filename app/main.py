from fastapi import FastAPI
from app.database.database import base,engine
from app.routes.user import router
from app.routes.project import project_route
from app.routes.tasks import task_route

base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Enterprise TaskOps API",
    description=(
        "A high-performance backend task management system built with FastAPI,"
        " SQLAlchemy, and JWT Authentication."
    ),
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Users",
            "description": (
                "Operations for user registration, login, profile, and"
                " authentication."
            ),
        },
        {
            "name": "projects",
            "description": (
                "Manager-level project creation, viewing, updating, and"
                " deletion."
            ),
        },
        {
            "name": "task",
            "description": (
                "Task operations, multi-employee assignments, status updates,"
                " and employee views."
            ),
        },
        {"name": "General", "description": "API health check and root endpoint."},
    ],
)
app.include_router(router=router)
app.include_router(router=project_route)
app.include_router(router=task_route)

@app.get("/", tags=["General"])
def home():
    return {"message": "Welcome to Enterprise TaskOps API"}