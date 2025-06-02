from enum import Enum
from sqlalchemy import Column,and_, or_, Integer, String, Boolean, DateTime, ForeignKey,Enum as SQLAlchemyEnum
from datetime import datetime
from .database import Base  
from .jobs import jobs
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship, foreign
from models.notificationComplaint import NotificationComplaint

class AppStatus(Enum):
    SUBMITTED = "SUBMITTED"
    REVIEWING = "REVIEWING"
    SHORTLISTED = "SHORTLISTED"
    INTERVIEWING = "INTERVIEWING"
    OFFERED = "OFFERED"
    REJECTED = "REJECTED"
    
class applications(Base):  #  user may post more than one jobs
    __tablename__ = 'applications'  #  
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(50), nullable=False) #  like title of application letter
    narration = Column(String(500), nullable=False)  # like an application letter
    doc_1 = Column(String(200), nullable=True)  # path to doc on filesystem...may be empty
    doc_2 = Column(String(200), nullable=True)  # path to doc on filesystem...may be empty
    doc_3 = Column(String(200), nullable=True)  # path to doc on filesystem...may be empty
    image = Column(String(200), nullable=True)  # path to image on filesystem...may be empty
    suitable_price = Column(Integer, nullable=True)  #  amount expectations
    status =  Column(SQLAlchemyEnum(AppStatus), default=AppStatus.SUBMITTED, nullable=False) 
    rejection_reason = Column(String(500), nullable=True)  # reason for rejection
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    dateTimeUpdated = Column(DateTime, default=datetime.utcnow)
    deleted = Column(String(1), default='N')  #  Y or N
    job_id =  Column(Integer,  ForeignKey("jobs.id"),nullable= False) # associated with a job  
    user_id =  Column(Integer,  ForeignKey("users.id"), nullable= False) # must be a user (i.e. staff or student)
    job = relationship("jobs", back_populates="applications")  #  job associated with this application
    user = relationship("Users", back_populates="applications")  #  user associated with this application
    job_allocation = relationship("JobAllocation", back_populates="applications")  #  job allocation for the application
    notifications = relationship(
        'NotificationComplaint',
        primaryjoin= and_(
            id == foreign(NotificationComplaint.target_id), # <-- Correct use of foreign()
            NotificationComplaint.target_type == 'application'
        ),
        viewonly=True,
        uselist=True,
        order_by=NotificationComplaint.dateTimeCreated.desc()
    )
   
    
    
    __table_args__ = (
        UniqueConstraint('job_id', 'user_id', name='unique_user_per_job'),
    )
    
    
   