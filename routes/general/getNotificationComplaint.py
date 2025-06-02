from .router import router 
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
from utils.general.getNotificationComplaint import list_job_communications,list_all_communications

from models.database import get_db
from models.accounts import Users 
from schemas.general.notificationComplaint import NotificationComplaintResponseSchema 
from utils.general.authentication import get_current_user 

@router.get("/jobs/{job_id}/communications/", response_model=List[NotificationComplaintResponseSchema])
def get_job_communications(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user) 
):
    return list_job_communications(
        job_id=job_id,
        db=db,
        current_user=current_user
    )
    
    


@router.get("/communications/all", response_model=List[NotificationComplaintResponseSchema])
def get_all_job_communications(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user), 
    skip: int = 0,
    limit: int = 100
):
    return list_all_communications(
        db=db,
        skip=skip,
        limit=limit
    )