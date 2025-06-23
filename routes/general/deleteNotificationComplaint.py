from .router import router 
from fastapi import Depends
from sqlalchemy.orm import Session
from models.database import get_db
from schemas.users.user import User
from utils.general.authentication import get_current_user,user_required_roles
from utils.general.deleteNotificationComplaint import delete_communication,toggle_step_down_notification
from schemas.general.deletion import  SoftDeletion

@router.delete("/communications/{notification_id}", include_in_schema=True, response_model="")
def communication(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # Assuming this returns your SQLAlchemy Users model instance
):
    return delete_communication(
        notification_id=notification_id,
        db=db,
        current_user=current_user
    )
    
    

    
@router.patch("/toggle_step_down_notification/", include_in_schema=True, response_model="")          
async def do(notificationId: int, delStatus: SoftDeletion , db: Session = Depends(get_db),TheUser: User = Depends(user_required_roles(['admin']))):
   return toggle_step_down_notification(notificationId,delStatus,TheUser, db)



   