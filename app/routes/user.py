from app.database.database import get_db
from app.models.users import users
from app.schemas.users import user_signup, forgot_password_schema, userpost
from sqlalchemy.orm import session
from fastapi import HTTPException, APIRouter, Depends
from app.core.security import hash_password, verify_password, jwt_create, jwt_auth
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/create")
def create_account(payload: user_signup, user_post: userpost, db: session = Depends(get_db)):
    db_check = db.query(users).filter(payload.email == users.email).first() or db.query(users).filter(payload.mobile_number == users.mobile_number).first()

    if db_check:
        raise HTTPException(status_code=400, detail="email or mobile number is already taken")

    if len(payload.mobile_number) != 10:
        raise HTTPException(status_code=400, detail="enter valid mobile number")

    hashed = hash_password(payload.password)
    db_load = users(name = payload.name,
                    mobile_number = payload.mobile_number,
                    email = payload.email,
                    password = hashed,
                    user_post = user_post)

    db.add(db_load) 
    db.commit()
    db.refresh(db_load)

    return (f"you have successfully registered for {user_post} role")

@router.post("/login")
def login_account(user: OAuth2PasswordRequestForm = Depends(), db : session = Depends(get_db)):
    db_check = db.query(users).filter(user.username == users.email).first()
    if db_check:
        verify = verify_password(user.password, db_check.password)
        if verify:
            token = jwt_create(data={'sub' : db_check.email,
                                      'post' : db_check.user_post,
                                      'user_id' : db_check.user_id})
            return {"access_token" : token, "token_type" : "bearer"}
    else:
        raise HTTPException(status_code=400 , detail="you are not registered")

@router.put("/forgot")
def forgot_password (user:forgot_password_schema, db:session = Depends(get_db)):
    db_check = db.query(users).filter(users.email == user.email).first()
    if db_check:
        hashed = hash_password(user.new_password)
        db_check.password = hashed

        db.commit()
        db.refresh(db_check)
        return("your password has been updated")
    else:
        raise HTTPException(status_code=404, detail="email not found")