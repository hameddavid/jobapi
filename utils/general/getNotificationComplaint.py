from fastapi import  HTTPException, status
from sqlalchemy.orm import Session,selectinload
from sqlalchemy import select

from models.notificationComplaint import NotificationComplaint 
from models.jobs import jobs 
from models.accounts import Users 



def list_job_communications(
    job_id: int,
    db: Session,
    current_user: Users
    ):
   try:
        # 1. Check if the job exists
        job = db.execute(select(jobs).where(jobs.id == job_id)).scalar_one_or_none()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job with ID {job_id} not found."
            )

        communications = db.execute(
        select(NotificationComplaint)
        .where(
            NotificationComplaint.target_type == 'job',
            NotificationComplaint.target_id == job_id
        )
        .order_by(NotificationComplaint.dateTimeCreated.desc())
        .options(selectinload(NotificationComplaint.receipts))  # Eagerly load the receipts
    ).scalars().all()


        return communications
   except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error {e}"
        )
        
        

def list_all_communications(
    db: Session,
    skip: int = 0,
    limit: int = 100
    ):
   try:

        communications = db.execute(
        select(NotificationComplaint)
        .order_by(NotificationComplaint.dateTimeCreated.desc())
        .options(selectinload(NotificationComplaint.receipts))  # Eagerly load the receipts
        .offset(skip).limit(limit)
    ).scalars().all()


        return communications
   except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error {e}"
        )