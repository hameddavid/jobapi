from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://accommodatedb:Mrsirl123@164.68.106.244:3306/dbjobs"
#engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})  
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()