from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer,Column,String
base=declarative_base()

class User(base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,autoincrement=True)
    name=Column(String(150),nullable=False)
    email=Column(String(150),nullable=False,unique=True)
    password_hash=Column(String(200),nullable=False)
    role=Column(String(50),default="student")
