from .router import router 
from fastapi import Depends
from sqlalchemy.orm import Session
from models.database import get_db
from models.accounts import Users 
from utils.general.authentication import get_current_user 
from utils.general.deleteNotificationComplaint import delete_communication

@router.delete("/communications/{notification_id}", include_in_schema=True, response_model="")
def communication(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user) # Assuming this returns your SQLAlchemy Users model instance
):
    return delete_communication(
        notification_id=notification_id,
        db=db,
        current_user=current_user
    )