from models.jobs import jobs as jobModel
from schemas.jobs.job import ListJobSchema
from schemas.jobs.jobCategorySchema import GetJobCategorySchema
from schemas.users.user import User as UserSchema
from fastapi import   HTTPException
from sqlalchemy.orm import Session 

def list_jobs(skip:int, limit:int, db: Session):
    try:
        jobQ = db.query(jobModel).offset(skip).limit(limit).all()
        if jobQ is None:
            raise HTTPException(status_code=404, detail=f"Jobs(skip={skip}, limit={limit}) not found")
        lstJobs: list[ListJobSchema]= []
        for job in jobQ:
        
            job_owner = UserSchema(id = job.owner.id, username = job.owner.username, emailAddy = job.owner.emailAddy,
                    firstname = job.owner.firstname, lastname = job.owner.lastname,
                    middlename = job.owner.middlename, dateCreated = job.owner.dateTimeCreated,) 

            cat_owner = UserSchema(id = job.job_category.user.id, username = job.job_category.user.username, emailAddy = job.job_category.user.emailAddy,
                    firstname = job.job_category.user.firstname, lastname = job.job_category.user.lastname,
                    middlename = job.job_category.user.middlename, dateCreated = job.job_category.user.dateTimeCreated,) 
            
            _category = GetJobCategorySchema(id = job.job_category.id, name = job.job_category.name, description = job.job_category.description,
                    deleted = job.job_category.deleted, createdBy = cat_owner,
                    createdAt = job.job_category.createdAt, updatedAt = job.job_category.updatedAt)
            
            ThisJob =  ListJobSchema(id = job.id, title = job.title, description = job.description, listed_price = job.listed_price,
                    location = job.location, owner = job_owner, category = _category,
                    dateTimeCreated = job.dateTimeCreated, status = job.status, deleted = job.deleted)
            lstJobs.append(ThisJob)
        if not lstJobs:
            raise HTTPException(status_code=404, detail=f"Jobs(skip={skip}, limit={limit}) not found")
        return lstJobs
    except Exception as e:       
        raise HTTPException(status_code=404, detail=f"Error listing job(s) : {str(e)})") 

  