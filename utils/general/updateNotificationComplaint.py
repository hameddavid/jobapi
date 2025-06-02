
from fastapi import  HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas.general.notificationComplaint import NotificationComplaintUpdateSchema, NotificationComplaintType, RecipientRole
from schemas.users.user import User
from models.notificationComplaint import NotificationComplaint # SQLAlchemy ORM models
from utils.general.CreateNotificationComplaint import user_notification_receipts, get_target_model
from datetime import datetime, timezone 


def update_communication(
    notification_id: int,
    update_data: NotificationComplaintUpdateSchema,
    db: Session ,
    current_user: User  # Assuming this returns your SQLAlchemy Users model instance
):
    # 1. Fetch the existing notification
    notification = db.execute(
        select(NotificationComplaint).where(NotificationComplaint.id == notification_id)
    ).scalar_one_or_none()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification with ID {notification_id} not found."
        )
  
    # 2. Authorization Check: Only sender or an admin can update
    # Adjust this logic based on your specific authorization rules
    # (e.g., maybe admins can update anything, senders can only update their own)
    if  notification.sender_id != current_user.id  and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this notification."
        )

    try:

        # 3. Apply updates to the notification object
        # Iterate over the fields in update_data that have a value (are not None)
        # and apply them to the ORM object.
        
        for field, value in update_data.model_dump(exclude_unset=True).items():
            # Special handling for Enum types to store their string value
            if field == 'type' and isinstance(value, NotificationComplaintType):
                setattr(notification, field, value.value)
            elif field == 'recipient_role' and isinstance(value, RecipientRole):
                setattr(notification, 'recipient_type', value.value) # Map recipient_role to recipient_type in DB
            else:
                setattr(notification, field, value)

        # 4. Re-validate target_id existence if target_id or target_type is being updated
        if update_data.target_id is not None or update_data.target_type is not None:
            # Use the new values if provided, otherwise fall back to existing values
            current_target_id = update_data.target_id if update_data.target_id is not None else notification.target_id
            current_target_type = update_data.target_type if update_data.target_type is not None else notification.target_type

            if current_target_id is not None and current_target_type is not None:
                TargetModel = get_target_model(current_target_type)
                if TargetModel is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Invalid target_type: {current_target_type}"
                    )
                
                target_obj_exists = db.execute(
                    select(TargetModel).where(TargetModel.id == current_target_id)
                ).scalar_one_or_none()

                if target_obj_exists is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Updated target {current_target_type} with ID {current_target_id} not found."
                    )
                        # user_notification_receipts
                if notification.type != update_data.type:
                    user_notification_receipts(
                        comm_data=update_data,
                        db=db,
                        target_obj=target_obj_exists,
                        notification=notification )
            # If target_id or target_type is being set to None, ensure logical consistency
            elif (update_data.target_id is None and update_data.target_type is not None) or (update_data.target_id is not None and update_data.target_type is None):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Both 'target_id' and 'target_type' must be provided or both omitted when updating."
                )

        # 5. Update updated_at timestamp
        notification.dateTimeUpdated = datetime.now(timezone.utc)
        
        # 6. Commit changes
        db.add(notification) # Add the modified object to the session (important for ORM tracking)
        db.commit()
        db.refresh(notification) # Refresh to get any database-generated values or updated timestamps

        return notification # Pydantic will serialize this ORM object using NotificationComplaintResponseSchema

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during update: {e}"
        )

