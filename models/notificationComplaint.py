from enum import Enum
from sqlalchemy import Text, Column, Integer, String, Boolean, DateTime, ForeignKey,Enum as SQLAlchemyEnum
from datetime import datetime
from .database import Base  
from sqlalchemy.orm import Session 
from typing import Optional, Union
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
# from models.accounts import  Users
# from models.jobs import jobs
# from models.applications import applications


class NotificationType(Enum):
    NOTIFICATION = "NOTIFICATION"
    COMPLAINT = "COMPLAINT"
    ALERT = "ALERT"
    BROADCAST_JOB = "BROADCAST_JOB"
    BROADCAST_APPLICATION = "BROADCAST_APPLICATION"
    
class RescipientType(Enum):
    JOB_OWNER = "JOB_OWNER"
    APPLICANT = "APPLICANT"
    ALL_APPLICANTS = "ALL_APPLICANTS"
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    STUDENT = "STUDENT"
    NONE = "NONE"  # For general system messages that don't target a specific user or job
    
    
    
class NotificationComplaint(Base):
    __tablename__ = 'notification_complaints'

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer,  ForeignKey("users.id"), nullable= False) # Or staff table
    subject = Column(String(255), nullable=False)
    message_body = Column(Text, nullable=False)
    type = Column(SQLAlchemyEnum(NotificationType), nullable=False)  # e.g., 'NOTIFICATION', 'COMPLAINT', 'ALERT'
    recipient_type = Column(SQLAlchemyEnum(RescipientType), nullable=False)  # e.g., 'JOB_OWNER', 'APPLICANT', 'ADMIN', etc.
    # Polymorphic target columns
    target_id = Column(Integer, nullable=True)  # Can be FK to job, application, or user
    target_type = Column(String(50), nullable=True) # 'job', 'application', 'user', 'none' for general system messages
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    dateTimeUpdated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship 
    sender = relationship('Users', back_populates='sent_notifications_complaints')
    receipts = relationship('UserNotificationReceipt', back_populates='notification', cascade="all, delete-orphan")


   

class UserNotificationReceipt(Base):
    __tablename__ = 'user_notification_receipts'
    
    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(Integer, ForeignKey('notification_complaints.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_read = Column(Boolean, default=False)
    readAt = Column(DateTime, nullable=True)  # Nullable if not read yet
    is_archived = Column(Boolean, default=False)
    archivedAt = Column(DateTime, nullable=True)  # Nullable if not archived yet
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    dateTimeUpdated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relationships
    notification = relationship('NotificationComplaint', back_populates='receipts')
    user = relationship('Users', back_populates='notification_receipts')