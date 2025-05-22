from fastapi import   HTTPException
from sqlalchemy.orm import Session
from schemas.users.user import User
from models.jobs import JobAllocation, jobs as jobModel
from datetime import datetime

from models.applications import applications as appModel


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
