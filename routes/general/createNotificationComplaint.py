from .router import router

from fastapi import Depends,status
from sqlalchemy.orm import Session
from models.database import get_db
from schemas.general.notificationComplaint import NotificationComplaintCreateSchema
from schemas.users.user import User 
from utils.general.authentication import get_current_user 
from utils.general.CreateNotificationComplaint import create_communication



@router.post("/communications/", status_code=status.HTTP_201_CREATED)
def communication(
    comm_data: NotificationComplaintCreateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    return  create_communication(
        comm_data=comm_data,
        current_user=current_user,
        db=db
    )