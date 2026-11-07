import bcrypt
from datetime import timedelta, datetime
from jose import jwt
from fastapi import HTTPException, Depends, status
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os
from sqlalchemy.orm import session
from app.database.database import get_db
from app.models.users import users

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def hash_password(password):
    hash = bcrypt.hashpw(password.encode('utf-8'),salt=bcrypt.gensalt())
    return hash.decode('utf-8')

def verify_password(password, hash):
    return bcrypt.checkpw(password.encode('utf-8'), hash.encode('utf-8'))


def jwt_create(data : dict, expires_delta : timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded

oauth = OAuth2PasswordBearer(tokenUrl="/users/login")
    
def jwt_auth(token:str =Depends(oauth), db: session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=401, detail="unauthorized")
    try:

        payload = jwt.decode(token, secret_key, algorithms=ALGORITHM)
        email : str = payload.get('sub')
        post : str = payload.get('post')
        
        if email is None:
            raise credentials_exception
    
    except:
        raise credentials_exception


    check = db.query(users).filter(users.email == email).first()
    if check is None:
        raise credentials_exception
    return {
        "email" : email,
        "post" : post,
        "user_id" : check.user_id
    }