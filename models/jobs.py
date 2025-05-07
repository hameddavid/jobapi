from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey 
from datetime import datetime
from .database import Base  
from sqlalchemy.orm import Session 
from sqlalchemy.ext.hybrid import hybrid_property

from sqlalchemy.orm import relationship
class jobs(Base):  #  user may post more than one jobs
    __tablename__ = 'jobs'  #  
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(50), nullable=False) #  
    description = Column(String(200), nullable=False)  #
    location = Column(String(50), nullable=False)  #  location of the job
    listed_price = Column(Integer, nullable=False)  #  price of the job
    status = Column(Integer,default=0)  #  job is closed by default until admin opens it
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    user_id =  Column(Integer,  ForeignKey("users.id"), nullable= False) # must be a user (i.e. staff or student)
    job_category_id = Column(Integer, ForeignKey("jobCategory.id"), nullable= False)  #  job category
    deleted = Column(String(1), default='N')  #  job is deleted by default until admin deletes it
    owner = relationship("Users", back_populates="jobs")  #  user who posted the job
    job_category = relationship("jobCategory", back_populates="jobs")  #  job category
    
    
    def get_owner(self, db: Session):
        """Gets user associated with this job."""
        return self.owner
    def get_job_category(self, db: Session):
        """Gets job category associated with this job."""
        return self.job_category
         
    


class jobCategory(Base):  #  Job category
    __tablename__ = 'jobCategory'  #  
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False) #  
    description = Column(String(200), nullable=True)  #
    deleted = Column(String(1), default='N')  #  
    createdBy = Column(Integer,  ForeignKey("users.id"), nullable= False)  #
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  #
    jobs = relationship("jobs", back_populates="job_category")  #  job category
    user = relationship("Users", back_populates="job_category")  #  user who created the job category
    
    @hybrid_property
    def is_deleted(self):
        return self.deleted == 'Y'

    @is_deleted.setter
    def is_deleted(self, value):
        self.deleted = 'Y' if value else 'N'