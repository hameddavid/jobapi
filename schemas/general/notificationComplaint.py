from pydantic import BaseModel,ConfigDict, Field, conint, constr, model_validator
from typing import Optional, Literal, List
from enum import Enum
from datetime import datetime



class NotificationComplaintType(str, Enum):
    NOTIFICATION = "NOTIFICATION"
    COMPLAINT = "COMPLAINT"
    ALERT = "ALERT"
    BROADCAST_JOB = "BROADCAST_JOB"
    BROADCAST_APPLICATION = "BROADCAST_APPLICATION"

class RecipientRole(str, Enum):
    JOB_OWNER = "JOB_OWNER"
    APPLICANT = "APPLICANT"
    ALL_APPLICANTS = "ALL_APPLICANTS"
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    NONE = "NONE"

class NotificationComplaintCreateSchema(BaseModel):
    subject: constr(min_length=5, max_length=255) = Field(...)
    message_body: constr(min_length=10) = Field(...)
    type: NotificationComplaintType = Field(...)

    target_id: Optional[conint(gt=0)] = Field(
        None, description="ID of the targeted entity (User, Job, or Application)."
    )
    target_type: Optional[Literal['user', 'job', 'application']] = Field(
        None, description="Type of the targeted entity ('user', 'job', or 'application')."
    )
    recipient_type: Optional[RecipientRole] = Field(None)

 
    model_config = ConfigDict(
        from_attributes=False, # Typically False for input schemas
        use_enum_values=True   # <--- ENSURE THIS IS TRUE!
        )

    @model_validator(mode='after')
    def validate_targeting_fields(self) -> 'NotificationComplaintCreateSchema':
        # Your existing conditional validation logic for target_id and target_type
        # (e.g., if type is COMPLAINT, then target_id and target_type must be present)
        # This ensures the *presence* of the fields based on 'type'.
        # The *existence* in DB is handled below.

        if self.type in [NotificationComplaintType.COMPLAINT, NotificationComplaintType.NOTIFICATION]:
            if self.target_type not in ['user', 'job', 'application']:
                raise ValueError("For COMPLAINT or NOTIFICATION, 'target_type' must be 'user', 'job', or 'application'.")
            if self.target_id is None:
                raise ValueError("For COMPLAINT or NOTIFICATION, 'target_id' must be provided.")
            if self.recipient_type is None:
                self.recipient_type = RecipientRole.NONE # Default for direct messages
        elif self.type == NotificationComplaintType.BROADCAST_JOB:
            if self.target_type != 'job':
                raise ValueError("For BROADCAST_JOB, 'target_type' must be 'job'.")
            if self.target_id is None:
                raise ValueError("For BROADCAST_JOB, 'target_id' must be provided.")
            if self.recipient_type != RecipientRole.ALL_APPLICANTS:
                raise ValueError("For BROADCAST_JOB, 'recipient_type' must be 'ALL_APPLICANTS'.")
        elif self.type == NotificationComplaintType.BROADCAST_APPLICATION:
            if self.target_type != 'application':
                raise ValueError("For BROADCAST_APPLICATION, 'target_type' must be 'application'.")
            if self.target_id is None:
                raise ValueError("For BROADCAST_APPLICATION, 'target_id' must be provided.")
            if self.recipient_type not in [RecipientRole.JOB_OWNER, RecipientRole.APPLICANT]:
                 raise ValueError("For BROADCAST_APPLICATION, 'recipient_type' must be 'JOB_OWNER' or 'APPLICANT'.")
        elif self.type == NotificationComplaintType.ALERT:
            if self.target_type is not None and self.target_id is None:
                 raise ValueError("If 'target_type' is provided for ALERT, 'target_id' must also be provided.")
            # If target_type is None, it's a general alert, no target_id needed.

        return self
    
    
    
    
class NotificationComplaintUpdateSchema(NotificationComplaintCreateSchema):
    subject: Optional[constr(min_length=5, max_length=255)] = Field(
        None, example="Updated Complaint Subject"
    )
    message_body: Optional[constr(min_length=10)] = Field(
        None, example="Updated message body for the complaint."
    )
    type: Optional[NotificationComplaintType] = Field( # Make it Optional
        None, example=NotificationComplaintType.ALERT
    )



class UserNotificationReceiptSchema(BaseModel):
    id: int
    notification_id: int
    user_id: int # ID of the recipient user
    is_read: bool
    readAt: Optional[datetime] = None  # Nullable if not read yet
    is_archived: bool = False  # Default to False
    archivedAt: Optional[datetime] = None  # Nullable if not archived yet
    dateTimeCreated: datetime
    dateTimeUpdated: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
    
    
    

class NotificationComplaintResponseSchema(BaseModel):
    id: int
    sender_id: int # Just the ID for now
    subject: str
    message_body: str
    type: NotificationComplaintType # Pydantic will serialize Enum to its value string
    
    target_id: Optional[int] = None
    target_type: Optional[str] = None # Will be 'user', 'job', or 'application'
    recipient_type: Optional[RecipientRole] = None # This is the column name in DB, maps from Pydantic's recipient_role

    dateTimeCreated: datetime
    dateTimeUpdated: datetime

    # Optional: If you want to include a nested representation of the sender
    # sender: UserBaseSchema # Requires loading the sender relationship in your query

    # Optional: If you want to include a list of associated receipts (be careful with N+1)
    receipts: List[UserNotificationReceiptSchema] = [] # Requires loading the receipts relationship

    model_config = ConfigDict(from_attributes=True)