from pydantic import BaseModel

class projects(BaseModel):
    project_title : str
    project_description : str
    
class get_projects_response(BaseModel):
    project_id : int
    project_title : str
    project_description :str
    created_by: int or str
    
class edit_project_schema(BaseModel):
    project_title : str or None
    project_description :str or None
