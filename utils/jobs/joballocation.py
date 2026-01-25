from fastapi import   HTTPException
from sqlalchemy.orm import Session
from schemas.users.user import User
from models.jobs import JobAllocation, jobs as jobModel, JobStatus
from datetime import datetime

from models.applications import applications as appModel, AppStatus


def allocate_job(app_id: int, ThisUser:User, db: Session ):  
    try:
        getApp = db.query(appModel).filter(appModel.id == app_id, appModel.status == 'SUBMITTED').first()
        if not getApp:
            raise HTTPException(status_code=404, detail=f"No application found for ID {app_id} or application status is not right for allocation")
        if getApp.user_id != ThisUser.id:
            raise HTTPException(status_code=403, detail="Oh no! You are not authorized to allocate this job")
        newApp = JobAllocation(
            application_id = getApp.id,
            dateTimeJobStarted = datetime.utcnow(),
            dateTimeJobCompleted = None,
            dateTimeJobClosed = None,
            dateTimePaymentMade = None,
            dateTimePaymentConfirmed = None,
            paymentReceiptURL = None,
            dateTimeCreated = datetime.utcnow(),
            dateTimeUpdated = datetime.utcnow(),
            deleted = 'N'
        )
        getJob = db.query(jobModel).filter(jobModel.id == getApp.job_id, jobModel.status=='OPEN').first()
        if not getJob:
            raise HTTPException(status_code=404, detail=f"No job found for ID {getApp.job_id} or job is not open")
        getJob.status = "ALLOCATED"
        getJob.dateTimeUpdated = datetime.utcnow()
        getApp.status = "OFFERED"
        getApp.dateTimeUpdated = datetime.utcnow()
        db.add(newApp)
        db.commit()
        db.refresh(newApp)
        # Notify the applicant about the allocation here
        return newApp
    except Exception as e:    
        db.rollback()   
        raise HTTPException(status_code=404, detail=f"Allocating job : {str(e)})") 


def deallocate_job(app_id: int, ThisUser: User, db: Session):
    """
    Deallocate a job allocation.
    - Admin users can deallocate any status
    - Job owners can only deallocate if the applicant has not accepted the offer
    - Job status will be returned to "PENDING"
    - Application status will be turned to "REVIEWING"
    """
    try:
        # Get the application
        getApp = db.query(appModel).filter(appModel.id == app_id).first()
        if not getApp:
            raise HTTPException(status_code=404, detail=f"No application found for ID {app_id}")
        
        # Get the job
        getJob = db.query(jobModel).filter(jobModel.id == getApp.job_id).first()
        if not getJob:
            raise HTTPException(status_code=404, detail=f"No job found for application ID {app_id}")
        
        # Check if user is admin or job owner
        is_admin = "admin" in ThisUser.roles
        is_job_owner = getJob.user_id == ThisUser.id
        
        if not is_admin and not is_job_owner:
            raise HTTPException(
                status_code=403, 
                detail="You are not authorized to deallocate this job. Only admins or job owners can perform this action."
            )
        
        # If not admin, check if application has been accepted
        if not is_admin and getApp.status == AppStatus.ACCEPTED:
            raise HTTPException(
                status_code=403, 
                detail="Cannot deallocate job. The applicant has already accepted the offer. Only admins can deallocate accepted offers."
            )
        
        # Get the job allocation
        getAllocation = db.query(JobAllocation).filter(
            JobAllocation.application_id == app_id, 
            JobAllocation.deleted == 'N'
        ).first()
        
        if not getAllocation:
            raise HTTPException(
                status_code=404, 
                detail=f"No active job allocation found for application ID {app_id}"
            )
        
        # Update job status to PENDING
        getJob.status = JobStatus.PENDING
        getJob.dateTimeUpdated = datetime.utcnow()
        
        # Update application status to REVIEWING
        getApp.status = AppStatus.REVIEWING
        getApp.dateTimeUpdated = datetime.utcnow()
        
        # Mark allocation as deleted
        getAllocation.deleted = 'Y'
        getAllocation.dateTimeUpdated = datetime.utcnow()
        
        db.commit()
        db.refresh(getApp)
        db.refresh(getJob)
        
        return {
            "message": "Job deallocated successfully",
            "application_id": app_id,
            "job_id": getJob.id,
            "new_job_status": getJob.status.value,
            "new_application_status": getApp.status.value
        }
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deallocating job: {str(e)}")


def accept_job_offer(app_id: int, ThisUser: User, db: Session):
    """
    Accept a job offer.
    - Only the applicant (user who applied) can accept the offer
    - Application must be in "OFFERED" status
    - Application status will be set to "ACCEPTED"
    - Job status will be set to "IN_PROGRESS"
    """
    try:
        # Get the application
        getApp = db.query(appModel).filter(appModel.id == app_id).first()
        if not getApp:
            raise HTTPException(status_code=404, detail=f"No application found for ID {app_id}")
        
        # Verify the current user is the applicant
        if getApp.user_id != ThisUser.id:
            raise HTTPException(
                status_code=403, 
                detail="You are not authorized to accept this job offer. Only the applicant can accept."
            )
        
        # Check if application status is OFFERED
        if getApp.status != AppStatus.OFFERED:
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot accept job offer. Application status must be 'OFFERED', but current status is '{getApp.status.value}'"
            )
        
        # Get the job
        getJob = db.query(jobModel).filter(jobModel.id == getApp.job_id).first()
        if not getJob:
            raise HTTPException(status_code=404, detail=f"No job found for application ID {app_id}")
        
        # Verify job allocation exists
        getAllocation = db.query(JobAllocation).filter(
            JobAllocation.application_id == app_id,
            JobAllocation.deleted == 'N'
        ).first()
        
        if not getAllocation:
            raise HTTPException(
                status_code=404,
                detail=f"No active job allocation found for application ID {app_id}"
            )
        
        # Update application status to ACCEPTED
        getApp.status = AppStatus.ACCEPTED
        getApp.dateTimeUpdated = datetime.utcnow()
        
        # Update job status to IN_PROGRESS
        getJob.status = JobStatus.IN_PROGRESS
        getJob.dateTimeUpdated = datetime.utcnow()
        
        db.commit()
        db.refresh(getApp)
        db.refresh(getJob)
        
        return {
            "message": "Job offer accepted successfully",
            "application_id": app_id,
            "job_id": getJob.id,
            "application_status": getApp.status.value,
            "job_status": getJob.status.value
        }
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error accepting job offer: {str(e)}")
