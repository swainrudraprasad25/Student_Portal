from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from os import getenv

load_dotenv()
db_user=getenv("db_user")
db_password=getenv("db_password")
url=f"mysql+pymysql://{db_user}:{db_password}@localhost:3306/portal_db"
engine=create_engine(url)
LocalSession=sessionmaker(bind=engine,autoflush=True)
def get_db():
    db=LocalSession()
    try:
        yield db
    finally:
        db.close()
