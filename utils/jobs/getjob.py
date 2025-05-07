from models.jobs import jobs as jobModel
from schemas.jobs.job import Job as JobSchema
from fastapi import   HTTPException
from sqlalchemy.orm import Session 

def list_jobs(skip:int, limit:int, db: Session):
    jobQ = db.query(jobModel).offset(skip).limit(limit).all()
    if jobQ is None:
        raise HTTPException(status_code=404, detail=f"Jobs(skip={skip}, limit={limit}) not found")
    lstJobs: list[JobSchema]= []
    for job in jobQ:
        ThisJob =  JobSchema(id = job.id, title = job.title, description = job.description, listed_price = job.listed_price,
                location = job.location, user_id = job.user_id, job_category_id = job.job_category_id,
                dateTimeCreated = job.dateTimeCreated, status = job.status, deleted = job.deleted)
        lstJobs.append(ThisJob)
    if not lstJobs:
        raise HTTPException(status_code=404, detail=f"Jobs(skip={skip}, limit={limit}) not found")
    return lstJobs


