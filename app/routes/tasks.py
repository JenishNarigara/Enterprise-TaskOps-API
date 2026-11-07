from app.database.database import get_db
from app.models.task import tasks as task_model , statusenum, task_assignee
from app.models.users import users
from app.schemas.task import task_model as task_schema,assign_schema, task_edit as task_edit_schema, view_project_task, statusenum
from app.core.security import jwt_auth
from sqlalchemy.orm import session
from fastapi import APIRouter, HTTPException, Depends

task_route = APIRouter(prefix="/task", tags=["task"])


@task_route.get("/{task_id}/status")
def check_task_status(task_id : int, auth = Depends(jwt_auth), db:session=Depends(get_db)):
    if auth["post"] == "manager":
        try:
            db_check = db.query(task_model).filter(task_model.task_id == task_id).first()
            status = db_check.task_status
            return (f"the status is : {status}")
        except:
            raise HTTPException(status_code=404, detail="task not found")
    else:
        raise HTTPException(status_code=403, detail="forbidden")

@task_route.get("/{project_id}", response_model=list[view_project_task] or None)
def view_all_tasks(project_id : int, auth = Depends(jwt_auth), db:session=Depends(get_db),):
    if auth["post"] == "manager":
        try:
            db_check = db.query(task_model).filter(task_model.project_id == project_id).all()
            if db_check:
                return db_check
            elif db_check == []:
                raise HTTPException(status_code=404, detail="no tasks assigned")
        except:
            raise HTTPException(status_code=404, detail="project id not found")
    else:
        raise HTTPException(status_code=403, detail="forbidden")

@task_route.get("/", response_model=list[view_project_task] or None)
def specific_status_tasks(status: statusenum, auth = Depends(jwt_auth), db:session=Depends(get_db)):
    if auth["post"] == "manager":
        try:
            db_check = db.query(task_model).filter(task_model.task_status == status).all()
            if db_check:
                return db_check
            elif db_check == []:
                raise HTTPException(status_code=404, detail="no tasks found")
        except:
            raise HTTPException(status_code=404, detail="no tasks found")
    else:
            raise HTTPException(status_code=403, detail="forbidden")

@task_route.get("/my-tasks/", response_model=list[view_project_task])
def emloyee_tasks(auth = Depends(jwt_auth), db:session=Depends(get_db)):
    if auth["post"] == "employee" :
        db_check = db.query(users).filter(users.user_id == auth["user_id"]).first()
        try:
            if db_check == []:
                return db_check.assigned_tasks
            else:
                raise Exception
        except:
            raise HTTPException(status_code=200, detail="you dont have any work")
    else:
        raise HTTPException(status_code=403, detail="forbidden")

@task_route.post("/create")
def create_task(user_input : task_schema,status : statusenum, payload = Depends(jwt_auth), db:session=Depends(get_db)):
    if payload["post"] == "manager":
        try :
            load_db = task_model(task_title = user_input.task_title,
                                 task_status = status,
                                 project_id = user_input.project_id,
                                 task_description= user_input.task_description)
            db.add(load_db)
            db.commit()
            db.refresh(load_db)

            return (f"your task {user_input.task_title} has been added to task")
        
        except:
            raise HTTPException(status_code=404, detail="project id not found")
    else:
        raise HTTPException(status_code=403, detail="forbidden")

@task_route.post("/{task_id}/assign")
def assign_task(task_id : int, assign_id : assign_schema, payload = Depends(jwt_auth), db:session=Depends(get_db)):
    if payload["post"] == "manager":
        db_check = db.query(task_model).filter(task_id == task_model.task_id).first()
        if db_check:
            employees = db.query(users).filter(users.user_id.in_(assign_id.assign_id)).all()
            if not employees:
                raise HTTPException(status_code=404, detail="employees not found")
            db_check.assignees = employees
            db.commit()
            db.refresh(db_check)
            return("task assigned to employees")
        
        else:
            raise HTTPException(status_code=404, detail="invalid task id")
    else:
        raise HTTPException(status_code=403 , detail="forbidden")

@task_route.put("/{task_id}/update")
def edit_task(task_id : int,status : statusenum, payload :task_edit_schema, auth = Depends(jwt_auth), db : session =Depends(get_db)):
    if auth["post"] == "manager":
        db_check = db.query(task_model).filter(task_model.task_id == task_id).first()
        if db_check:
            if payload.task_title != "string" or payload.task_title is not None:
                db_check.task_title = payload.task_title
            if payload.task_description != "string" or payload.task_title is not None:
                db_check.task_description = payload.task_description
            db_check.task_status = status
            db.commit()
            db.refresh(db_check)
            return ("database has been updated successfully")
        else:
            raise HTTPException(status_code=404 , detail="task id is invalid")
    else:
        raise HTTPException(status_code=403 , detail="forbidden")

@task_route.put("/{task_id}/update-status")
def update_task_status(task_id : int,payload: statusenum , auth = Depends(jwt_auth), db:session = Depends(get_db)):
    if auth["post"] == "employee" :
        db_update = db.query(task_model).filter(task_model.task_id == task_id).first()
        if db_update:
            db_update.task_status = payload
            db.commit()
            db.refresh(db_update)
            return ("status of task has been updated")
        else:
            raise HTTPException(status_code=404, detail="invelid task id")
    else:
        raise HTTPException(status_code=403, detail="forbidden")

@task_route.delete("/{task_id}/delete")
def delete_task(task_id :int, auth = Depends(jwt_auth), db:session= Depends(get_db)):
    if auth["post"] == "manager":
        db_delete = db.query(task_model).filter(task_model.task_id == task_id).first()
        if db_delete :
            db.delete(db_delete)
            db.commit()
            return(f"{task_id} has been deleted successfully")
        else:
            return("invalid task id")
    else:
        raise HTTPException(status_code=403, detail="forbidden")