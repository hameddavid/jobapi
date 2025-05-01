from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey 
from datetime import datetime
from .database import Base  
from .jobs import jobs
class applications(Base):  #  user may post more than one jobs
    __tablename__ = 'applications'  #  
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(50), nullable=False) #  like title of application letter
    narration = Column(String(500), nullable=False)  # like an application letter
    doc_1 = Column(String(200), nullable=True)  # path to doc on filesystem...may be empty
    doc_2 = Column(String(200), nullable=True)  # path to doc on filesystem...may be empty
    doc_3 = Column(String(200), nullable=True)  # path to doc on filesystem...may be empty
    image = Column(String(200), nullable=True)  # path to image on filesystem...may be empty
    status = Column(Integer,default=1)  #  0 -> deactivated , 1 -> activated
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    job_id =  Column(Integer,  ForeignKey("jobs.id"), unique=True,nullable= False) # associated with a job  
    user_id =  Column(Integer,  ForeignKey("users.id"), nullable= False) # must be a user (i.e. staff or student)