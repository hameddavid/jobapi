from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.jobs.job import JobUpdate

from models.jobs import jobs as jobModel, JobStatus
from models.applications import applications as appModel, AppStatus

def update_job(jobData: JobUpdate, TheUser, db: Session):
     try:
          jobQ = db.query(jobModel).filter(jobModel.id == jobData.id).first()
          if jobQ is None:
               raise HTTPException(status_code=404, detail=f"Job with id {jobData.id} not found or does not belong to the user.")
          else:
               if jobQ.user_id != TheUser.id and "admin" not in TheUser.roles:
                    raise HTTPException(status_code=403, detail="You do not have permission to update this job category.")
               if jobData.title is not None:
                    jobQ.title = jobData.title
               if jobData.description is not None:
                    jobQ.description = jobData.description
               if jobData.location is not None:
                    jobQ.location = jobData.location
               if jobData.listed_price is not None:
                    jobQ.listed_price = jobData.listed_price
               if jobData.status is not None:
                    jobQ.status = jobData.status
               if jobData.cat_id is not None:
                    jobQ.job_category_id = jobData.cat_id
               if jobData.deleted is not None:
                    jobQ.deleted = jobData.deleted
               db.commit()
               db.refresh(jobQ)
               return jobQ
     except Exception as e:
          raise HTTPException(status_code=404, detail=f"Error updating job: {str(e)})")


# Endpoint 1: Set job status to COMPLETED (applicant or admin)

def set_job_completed(job_id: int, TheUser, db: Session):
     jobQ = db.query(jobModel).filter(jobModel.id == job_id).first()
     if jobQ is None:
          raise HTTPException(status_code=404, detail=f"Job with id {job_id} not found.")

     # Find application for this job with status OFFERED or ACCEPTED
     appQ = db.query(appModel).filter(
          appModel.job_id == job_id,
          appModel.status.in_([AppStatus.OFFERED, AppStatus.ACCEPTED])
     ).first()
     if appQ is None:
          raise HTTPException(status_code=404, detail="No application with status OFFERED or ACCEPTED for this job.")

     # Only the user of this application (doer) or admin can set to completed
     if TheUser.id != appQ.user_id and "admin" not in TheUser.roles:
          raise HTTPException(status_code=403, detail="You do not have permission to set this job as completed.")

     jobQ.status = JobStatus.COMPLETED
     db.commit()
     db.refresh(jobQ)
     return jobQ


# Endpoint 2: Accept or reject completed job (owner or admin), with optional comment
def owner_accept_reject_completed_job(job_id: int, jStatus: JobStatus, TheUser, db: Session, comment: str = None):
     jobQ = db.query(jobModel).filter(jobModel.id == job_id).first()
     if jobQ is None:
          raise HTTPException(status_code=404, detail=f"Job with id {job_id} not found.")
     # Only job owner or admin can accept/reject
     if TheUser.id != jobQ.user_id and "admin" not in TheUser.roles:
          raise HTTPException(status_code=403, detail="You do not have permission to accept/reject this job.")
     if jobQ.status != JobStatus.COMPLETED:
          raise HTTPException(status_code=400, detail="Job must be in COMPLETED status to accept or reject.")
     
     jobQ.status = jStatus.value
     if comment:
          jobQ.comments = comment
   
     db.commit()
     db.refresh(jobQ)
     return jobQ



