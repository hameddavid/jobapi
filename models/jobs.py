from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey 
from datetime import datetime
from .database import Base  
class jobs(Base):  #  user may post more than one jobs
    __tablename__ = 'jobs'  #  
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(50), nullable=False) #  
    description = Column(String(200), nullable=False)  #
    status = Column(Integer,default=0)  #  job is closed by default until admin opens it
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    user_id =  Column(Integer,  ForeignKey("users.id"), nullable= False) # must be a user (i.e. staff or student)