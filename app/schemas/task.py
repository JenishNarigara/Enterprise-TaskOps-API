from pydantic import BaseModel
from app.models.task import statusenum

class task_model(BaseModel):
    task_title : str
    project_id : int
    task_description : str

class assign_schema(BaseModel):
    assign_id : list[int]

class task_edit(BaseModel):
    task_title : str or None
    task_description : str or None  

class view_project_task(BaseModel):
    task_id : int
    task_title : str
    task_description : str
    task_status : statusenum
    project_id : int

