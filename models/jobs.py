from enum import Enum
from sqlalchemy import Column,and_, or_, DateTime, Text,Integer, String, Boolean, DateTime, ForeignKey,UniqueConstraint,Enum as SQLAlchemyEnum
from datetime import datetime
from .database import Base  
from sqlalchemy.orm import Session 
from sqlalchemy.ext.hybrid import hybrid_property
from models.notificationComplaint import NotificationComplaint
from sqlalchemy.orm import relationship, foreign

class JobStatus(Enum):
    ACCEPTED = "ACCEPTED"
    ALLOCATED = "ALLOCATED"
    ARCHIVED = "ARCHIVED"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    AWAITING_PAYMENT = "AWAITING_PAYMENT"
    CLOSED = "CLOSED"
    COMPLETED = "COMPLETED"
    DELETED = "DELETED"
    IN_PROGRESS = "IN_PROGRESS"
    OPEN = "OPEN"
    PAID = "PAID"
    PENDING = "PENDING"
    REJECTED = "REJECTED"
    SUBMITTED = "SUBMITTED"

class jobs(Base):  #  user may post more than one jobs
    __tablename__ = 'jobs'  #  
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(50), nullable=False) #  
    description = Column(String(200), nullable=False)  #
    keywords = Column(String(200), nullable=False)  #  keywords for the job
    location = Column(String(50), nullable=False)  #  location of the job
    listed_price = Column(Integer, nullable=False)  #  price of the job
    status = Column(SQLAlchemyEnum(JobStatus), default=JobStatus.SUBMITTED, nullable=False)  #  job is closed by default until admin opens it
    doc_1 = Column(String(200), nullable=True)
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    dateTimeUpdated = Column(DateTime, default=datetime.utcnow)
    user_id =  Column(Integer,  ForeignKey("users.id"), nullable= False) # must be a user (i.e. staff or student)
    job_category_id = Column(Integer, ForeignKey("jobCategory.id"), nullable= False)  #  job category
    deleted = Column(String(1), default='N')  #  job is deleted by default until admin deletes it
    owner = relationship("Users", back_populates="jobs")  #  user who posted the job
    job_category = relationship("jobCategory", back_populates="jobs")  #  job category
    applications = relationship("applications", back_populates="job")  #  applications for the job
    notifications =  relationship(
        'NotificationComplaint',
        primaryjoin= and_(
            id == foreign(NotificationComplaint.target_id), # <-- Correct use of foreign()
            NotificationComplaint.target_type == 'application'
        ),
        viewonly=True,
        uselist=True,
        order_by=NotificationComplaint.dateTimeCreated.desc()
    )
    
    
    def get_owner(self, db: Session):
        """Gets user associated with this job."""
        return self.owner
    def get_job_category(self, db: Session):
        """Gets job category associated with this job."""
        return self.job_category
         
    

class JobAllocation(Base):
    #  user may post more than one jobs 
    __tablename__ = 'jobAllocation'  #
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey("applications.id"),unique=True, nullable=False) 
    dateTimeJobStarted = Column(DateTime, nullable=False)
    dateTimeJobCompleted = Column(DateTime, default=None)
    dateTimeJobClosed = Column(DateTime, default=None)
    proposedDateTimeJobClosed = Column(DateTime, default=None)
    dateTimePaymentMade = Column(DateTime, default=None)
    dateTimePaymentConfirmed = Column(DateTime, default=None)
    paymentReceiptURL = Column(String(200), nullable=True)  #  payment receipt
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    dateTimeUpdated = Column(DateTime, default=datetime.utcnow)
    applications = relationship("applications", back_populates="job_allocation")  
    deleted = Column(String(1), default='N') 

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
        





class RateType(Enum):
    OWNER = "OWNER"
    DOER = "DOER"


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    # These IDs refer to the roles in the Job itself, not necessarily the rater/rated in the rating
    job_doer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    rating = Column(Integer, nullable=False) # e.g., 1 to 5 stars
    review_text = Column(Text, nullable=True)
    rate_type = Column(SQLAlchemyEnum(RateType), nullable=False) # Distinguishes who is rating whom
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted = Column(String(1), default='N') 

    # --- CORRECTED __table_args__ for multiple UniqueConstraints ---
    __table_args__ = (
        # Constraint for Owner rating Doer:
        # Ensures that a specific job_owner (rater) can only rate a specific job_doer (rated) on a given job once,
        # specifically when the rating type is OWNER.
        UniqueConstraint('job_id', 'job_owner_id', 'job_doer_id', 'rate_type',
                         name='_owner_rates_doer_on_job_uc',
                         # Partial index for efficiency, only applies when rate_type is 'OWNER'
                         # This might be tricky to implement directly in SQLAlchemy for Enum if not using raw SQL
                         # Consider doing this check in application logic or with an explicit partial index in migration
                         # if ORM doesn't support it directly. For most databases, it works.
                         # postgresql_where=rate_type == RateType.OWNER # Example for PostgreSQL partial index
                        ),

        # Constraint for Doer rating Owner:
        # Ensures that a specific job_doer (rater) can only rate a specific job_owner (rated) on a given job once,
        # specifically when the rating type is DOER.
        UniqueConstraint('job_id', 'job_doer_id', 'job_owner_id', 'rate_type',
                         name='_doer_rates_owner_on_job_uc',
                         # postgresql_where=rate_type == RateType.DOER # Example for PostgreSQL partial index
                        ),
        # You can add other Index() or ForeignKeyConstraint() definitions here if needed
    )
    # ---------------------------------------------------------------

    # Relationships (ensure your 'Users' and 'jobs' models are defined elsewhere)
    job = relationship("jobs") # The job associated with this rating
    doer = relationship("Users", foreign_keys=[job_doer_id]) # The doer linked to this job instance
    owner = relationship("Users", foreign_keys=[job_owner_id]) # The owner linked to this job instance

    def __repr__(self):
        return (
            f"<Rating(id={self.id}, job_id={self.job_id}, "
            f"rater_type={self.rate_type.value}, "
            f"rating={self.rating}, "
            f"job_doer_id={self.job_doer_id}, "
            f"job_owner_id={self.job_owner_id})>"
        )
