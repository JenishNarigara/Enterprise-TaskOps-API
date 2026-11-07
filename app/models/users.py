from sqlalchemy import String, Boolean, Integer, Column, Enum as sqlnum
from app.database.database import base
import enum

class userpostenum(str,enum.Enum):
    manager = "manager"
    employee = "employee"

class users(base):
    __tablename__="employees"
    user_id = Column(Integer, primary_key=True, nullable=False ,unique=True ,autoincrement=True)
    name = Column(String(50), nullable=False)
    mobile_number = Column(String,nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False)
    user_post = Column(sqlnum(userpostenum), default=userpostenum.employee,nullable=False)
