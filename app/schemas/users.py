from pydantic import BaseModel, EmailStr
from enum import Enum

class userpost(str,Enum):
    manager = "manager"
    employee = "employee"

class user_signup(BaseModel):
    name : str
    mobile_number : str
    email : EmailStr
    password : str

class forgot_password_schema(BaseModel):
    email : EmailStr
    new_password : str