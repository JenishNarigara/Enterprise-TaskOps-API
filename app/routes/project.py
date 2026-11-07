from app.database.database import get_db
from app.models.project import  project
from app.schemas.project import projects, get_projects_response, edit_project_schema
from app.core.security import jwt_auth
from sqlalchemy.orm import session
from fastapi import APIRouter, HTTPException, Depends

project_route = APIRouter(prefix='/projects', tags=['projects'])

@project_route.get("/", response_model=list[get_projects_response])
def view_all_projects(auth = Depends(jwt_auth),db:session=Depends(get_db)):
    if auth["post"] == "manager":
        try:
            every_projects = db.query(project).all()
            
            return every_projects

        except:
            return("something went wrong")
    
    else :
        raise HTTPException(status_code=403, detail="forbidden")
    
@project_route.get("/{project_id}")
def view_specific_project (project_id : int ,auth = Depends(jwt_auth), db : session =Depends(get_db)):
    if auth["post"] == "manager":
        try:
            every_projects = db.query(project).filter(project.project_id == project_id).first()
                
            return every_projects
    
        except:
            return("something went wrong")
        
    else :
        raise HTTPException(status_code=403, detail="forbidden")
        
@project_route.post('/create')
def create_project(payload : projects , auth  =  Depends(jwt_auth) , db : session = Depends(get_db)):
    if auth["post"] == 'manager':
        try :
            db_load = project(project_title=payload.project_title,
                              project_description= payload.project_description,
                              created_by = auth["user_id"])
            db.add(db_load)
            db.commit()
            db.refresh(db_load)

            project_id = db.query(project).filter(payload.project_title == project.project_title).first()

            return(f"the project {project_id.project_title} has created successfully, project id is {project_id.project_id}")
        
        except:
            raise HTTPException(status_code=400 ,detail="project already exists")

    else:
        raise HTTPException(status_code=403 , detail="for bidden")
 

@project_route.put("/{project_id}/update")
def edit_project(project_id : int, payload : edit_project_schema, auth = Depends(jwt_auth), db:session=Depends(get_db)):
    if auth["post"] == "manager":
        db_update = db.query(project).filter(project.project_id == project_id).first()
        if db_update:
            try:
                if payload.project_title != "string":
                    db_update.project_title = payload.project_title
                if payload.project_description != "string":
                    db_update.project_description = payload.project_description
                db.commit()
                db.refresh(db_update)
                return ("database has been updated successfully")
            except:
                raise HTTPException (status_code=400, detail="project title already exists")
        else:
            raise HTTPException(status_code=404, detail="project id is invalid")
    else:
        raise HTTPException(status_code=403 , detail="forbidden")

@project_route.delete("/{project_id}/delete")
def delete_project(project_id : int, auth = Depends(jwt_auth), db:session=Depends(get_db)):
    if auth["post"] == "manager":
        db_delete = db.query(project).filter(project.project_id == project_id).first()
        if db_delete :
            db.delete(db_delete)
            db.commit()
            return(f"{project_id} has been deleted successfully")
        else:
            raise HTTPException(status_code=404, detail="invalid task id")
    else:
        raise HTTPException(status_code=403, detail="forbidden")
        