
from fastapi import  HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from schemas.general.notificationComplaint import NotificationComplaintCreateSchema, NotificationComplaintType, RecipientRole
from schemas.users.user import User
from models.accounts import Users, Admins 
from models.jobs import jobs 
from models.applications import applications 
from models.notificationComplaint import NotificationComplaint, UserNotificationReceipt # SQLAlchemy ORM models


from datetime import datetime, timezone 


def create_communication(
    comm_data: NotificationComplaintCreateSchema,
    current_user: User,
    db: Session 
):
    # Initialize target_obj outside the if block so it's accessible later
    target_obj = None 

    try:
        # 1. Database existence validation for target_id (no commit yet)
        if comm_data.target_id is not None and comm_data.target_type is not None:
            TargetModel = get_target_model(comm_data.target_type)
            if TargetModel is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid target_type: {comm_data.target_type}"
                )

            target_obj = db.execute(
                select(TargetModel).where(TargetModel.id == comm_data.target_id)
            ).scalar_one_or_none()

            if target_obj is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Target {comm_data.target_type} with ID {comm_data.target_id} not found."
                )
        
        # 2. Create the NotificationComplaint record (no commit yet)
        db_communication = NotificationComplaint(
            sender_id=current_user.id,
            subject=comm_data.subject,
            message_body=comm_data.message_body,
            type=comm_data.type, # Store Enum value as string
            target_id=comm_data.target_id,
            target_type=comm_data.target_type, # Store string value directly
            recipient_type=comm_data.recipient_type # Corrected: use recipient_type from schema
        )

        db.add(db_communication)
        # db.refresh(db_communication) # No need to refresh immediately, id will be available after commit
                                    # or after a flush if needed, but not common here.

        # At this point, db_communication is in the session, but not committed.
        # Its ID will be assigned after the first flush/commit.
        # To get the ID for receipts before commit, we need a flush:
        db.flush() # This assigns primary keys for newly added objects

        # 3. Efficiently populate user_notification_receipts based on type and recipient_type
        user_notification_receipts(comm_data, db, target_obj,db_communication)
        # --- FINAL COMMIT ---
        # Commit all changes to the database only if everything above was successful
        db.commit()
        db.refresh(db_communication) # Refresh to get latest state, including the ID if not already available

        return {"message": "Communication created successfully", "id": db_communication}

    except HTTPException as e:
        # Re-raise HTTPExceptions directly as they are expected errors
        db.rollback() # Rollback changes before re-raising
        raise HTTPException(status_code=404, detail=f"Issue : {str(e)})") 
    except Exception as e:
        # Catch any other unexpected errors and rollback
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )



def get_target_model(target_type: str):
    """Helper to get the SQLAlchemy model class based on target_type string."""
    if target_type == 'user':
        return Users
    elif target_type == 'job':
        return jobs
    elif target_type == 'application':
        return applications
    return None # Should be caught by Pydantic's Literal validation


def user_notification_receipts(comm_data: NotificationComplaintCreateSchema, db: Session, target_obj=None,db_communication=None):
        receipts_to_create = [] # Collect all receipts here for bulk insert

        if comm_data.type == NotificationComplaintType.COMPLAINT:
            recipient_user_ids = []
            if comm_data.recipient_type == RecipientRole.ADMIN:
                admin_users = db.execute(select(Admins.user_id).where(Admins.is_Active == True)).scalars().all()
                recipient_user_ids.extend(admin_users)
            elif comm_data.recipient_type == RecipientRole.JOB_OWNER and isinstance(target_obj, jobs):
                # Assuming Job model has a user_id foreign key for its owner
                if hasattr(target_obj, 'user_id') and target_obj.user_id:
                    recipient_user_ids.append(target_obj.user_id)
                else:
                    raise HTTPException(status_code=404, detail=f"Warning: Job {target_obj.id} does not have an associated owner_id for complaint.")
                    
            elif comm_data.target_type == 'user' and target_obj: 
                 recipient_user_ids.append(target_obj.id)

            for user_id in set(recipient_user_ids):
                receipts_to_create.append({
                    "notification_id": db_communication.id,
                    "user_id": user_id,
                    "is_read": False,
                    "dateTimeCreated": datetime.now(timezone.utc) # Store timezone-aware datetime
                })

        elif comm_data.type == NotificationComplaintType.NOTIFICATION:
            if comm_data.target_type == 'user' and target_obj:
                receipts_to_create.append({
                    "notification_id": db_communication.id,
                    "user_id": target_obj.id,
                    "is_read": False,
                    "dateTimeCreated": datetime.now(timezone.utc)
                })
            else:
                raise HTTPException(status_code=404, detail=f"Warning: Notification can't be created without a valid target user.")

        elif comm_data.type == NotificationComplaintType.BROADCAST_JOB:
            if target_obj and isinstance(target_obj, jobs) and comm_data.recipient_type == RecipientRole.ALL_APPLICANTS:
                applicant_user_ids = db.execute(
                    select(applications.user_id)
                    .where(applications.job_id == comm_data.target_id)
                ).scalars().all()

                for user_id in set(applicant_user_ids):
                    receipts_to_create.append({
                        "notification_id": db_communication.id,
                        "user_id": user_id,
                        "is_read": False,
                        "dateTimeCreated": datetime.now(timezone.utc)
                    })
                if not receipts_to_create:
                    raise HTTPException(status_code=404, detail=f"No applicants found for job ID {comm_data.target_id} to broadcast to.")

        elif comm_data.type == NotificationComplaintType.BROADCAST_APPLICATION:
            if target_obj and isinstance(target_obj, applications):
                recipient_user_id = None
                if comm_data.recipient_type == RecipientRole.APPLICANT:
                    recipient_user_id = target_obj.user_id
                elif comm_data.recipient_type == RecipientRole.JOB_OWNER:
                    # Assuming 'jobs' model has a 'user_id' field for the owner
                    job_owner_id = db.execute(select(jobs.user_id).where(jobs.id == target_obj.job_id)).scalar_one_or_none()
                    if job_owner_id:
                        recipient_user_id = job_owner_id

                if recipient_user_id:
                    receipts_to_create.append({
                        "notification_id": db_communication.id,
                        "user_id": recipient_user_id,
                        "is_read": False,
                        "dateTimeCreated": datetime.now(timezone.utc)
                    })
                else:
                    raise HTTPException(status_code=404, detail= "Warning: BROADCAST_APPLICATION can't be created because no valid recipient found.")

        elif comm_data.type == NotificationComplaintType.ALERT:
            if comm_data.target_type == 'user' and target_obj:
                receipts_to_create.append({
                    "notification_id": db_communication.id,
                    "user_id": target_obj.id,
                    "is_read": False,
                    "dateTimeCreated": datetime.now(timezone.utc)
                })
            else:
                raise HTTPException(status_code=404, detail="System-wide alert can't be created, no specific user receipts generated.")

        # Perform bulk insert for UserNotificationReceipts if there are any
        if receipts_to_create:
            db.execute(insert(UserNotificationReceipt).values(receipts_to_create))
            
