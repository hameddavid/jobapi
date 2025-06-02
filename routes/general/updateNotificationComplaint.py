from .router import router

from fastapi import Depends,status
from sqlalchemy.orm import Session
from models.database import get_db
from schemas.general.notificationComplaint import NotificationComplaintUpdateSchema
from schemas.users.user import User 
from utils.general.authentication import get_current_user 
from utils.general.updateNotificationComplaint import update_communication



@router.put("/communications/{notification_id}", response_model=NotificationComplaintUpdateSchema, status_code=status.HTTP_200_OK)
def communication(
    notification_id: int,
    update_data: NotificationComplaintUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    return  update_communication(
        notification_id=notification_id,
        update_data=update_data,
        current_user=current_user,
        db=db
    )