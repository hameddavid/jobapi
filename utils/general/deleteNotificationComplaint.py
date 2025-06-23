
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.notificationComplaint import NotificationComplaint 
from schemas.users.user import User
from schemas.general.deletion import SoftDeletion




def delete_communication(
    notification_id: int,
    db: Session ,
    current_user: User
):
    notification = db.execute(
        select(NotificationComplaint).where(NotificationComplaint.id == notification_id)
    ).scalar_one_or_none()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification with ID {notification_id} not found."
        )

    if notification.sender_id != current_user.id  and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this notification."
        )

    try:
        db.delete(notification)
        db.commit()
        return {"detail": "Notification/complaint deleted successfully"}
    
    except Exception as e:
        db.rollback() # Rollback changes if an error occurs
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during deletion: {e}"
        )
        
    
# toggle_step_down_notification


def toggle_step_down_notification(noti_id: int, delStatus: SoftDeletion ,TheUser:User, db: Session ):  
    try:
       notiObj = db.query(NotificationComplaint).filter(NotificationComplaint.id == noti_id).first()
       if notiObj is None:
           raise HTTPException(status_code=404, detail=f"Notification  with id {noti_id} not found.")
       if  "admin" not in TheUser.roles:
               # Check if the user is not the creator and is not an admin
           raise HTTPException(status_code=403, detail="You do not have permission to stepdown this notification.")
       
       notiObj.deleted = delStatus.value
       db.commit()
       db.refresh(notiObj)
       return notiObj
    except Exception as e:
        db.rollback()        
        raise HTTPException(status_code=404, detail=f"Toggling notification : {str(e)})") 