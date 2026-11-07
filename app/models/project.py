from sqlalchemy import Column, String, Integer, ForeignKey
from app.database.database import base

class project(base):
    __tablename__ = "projects"
    project_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    project_title = Column(String, unique=True, nullable=False)
    project_description = Column(String, nullable=False)
    created_by = Column(Integer, ForeignKey("employees.user_id"), nullable=False)

