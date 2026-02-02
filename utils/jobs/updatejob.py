from fastapi import   HTTPException
from sqlalchemy.orm import Session
from schemas.jobs.job import JobUpdate
from models.jobs import jobs as jobModel

def update_job(jobData:JobUpdate,TheUser, db: Session ):  
    
    try:
       jobQ = db.query(jobModel).filter(jobModel.id == jobData.id).first()
       if jobQ is None:
           raise HTTPException(status_code=404, detail=f"Job with id {jobData.id} not found or does not belong to the user.")
       else:
           if jobQ.user_id != TheUser.id and "admin" not in TheUser.roles:
               # Check if the user is not the creator and is not an admin
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

 

