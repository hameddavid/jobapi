from fastapi import   HTTPException
from sqlalchemy.orm import Session
from schemas.users.user import User
from schemas.jobs.job import JobCreate
from models.jobs import jobs as jobModel


def create_job(job: JobCreate, ThisUser:User, db: Session ):  
    try:
        newJob = jobModel(
            title = str(job.title).capitalize(),
            description =  str(job.description).capitalize(),
            listed_price = job.listed_price,
            location = job.location,
            keywords = job.keywords,
            job_category_id = job.cat_id,
            user_id = ThisUser.id
        )
        db.add(newJob)
        db.commit()
        db.refresh(newJob)
        return newJob
    except Exception as e:       
        raise HTTPException(status_code=404, detail=f"Error creating job : {str(e)})") 

    