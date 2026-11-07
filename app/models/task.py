from sqlalchemy import Column, String, Integer, ForeignKey, Enum as sqlnum, Table
from sqlalchemy.orm import relationship
from app.database.database import base
from enum import Enum

class statusenum (str, Enum):
    panding = "panding"
    in_progress = "in_progress"
    completed = "completed"

task_assignee = Table("task_assignee", base.metadata, 
                       Column("task_id", Integer,ForeignKey("tasks.task_id", ondelete="CASCADE"), primary_key=True, ),
                       Column("user_id", Integer, ForeignKey("employees.user_id", ondelete="CASCADE"), primary_key=True))

class tasks(base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    task_title = Column(String, nullable=False)
    task_description = Column(String, nullable=False)
    task_status = Column(sqlnum(statusenum), default=statusenum.panding, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    assignees = relationship("users", secondary=task_assignee, backref="assigned_tasks")
