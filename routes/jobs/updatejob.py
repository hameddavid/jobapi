from fastapi import  Depends, Body 
from sqlalchemy.orm import Session 
from utils.jobs.updatejob import   update_job, set_job_completed, owner_accept_reject_completed_job
from models.database import  get_db
from schemas.jobs.job import Job , JobUpdate
from models.jobs import  JobStatus
from schemas.users.user import User
from utils.general.authentication import get_current_user
from .router import router

   
@router.patch("/updateJob/", include_in_schema=True, response_model=Job)          
async def do(thisJob: JobUpdate = Body(..., embed= True), db: Session = Depends(get_db),
              TheUser: User = Depends(get_current_user)):
   return update_job(thisJob,TheUser, db)

@router.post("/setJobCompleted/{job_id}", include_in_schema=True, response_model=Job)
async def set_job_completed_endpoint(job_id: int, db: Session = Depends(get_db),
                                   TheUser: User = Depends(get_current_user)):
    return set_job_completed(job_id, TheUser, db)

@router.post("/ownerAcceptRejectCompletedJob/{job_id}", include_in_schema=True, response_model=Job)
async def owner_accept_reject_completed_job_endpoint(job_id: int, jStatus: JobStatus, comment: str = None, db: Session = Depends(get_db),
                                   TheUser: User = Depends(get_current_user)):
    return owner_accept_reject_completed_job(job_id, jStatus, TheUser, db, comment)
