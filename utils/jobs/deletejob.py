from fastapi import   HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.jobs import  jobs
from models.applications import applications




def delete_job(job_id: int,TheUser, db: Session ):  
    
    try:
       job = db.query(jobs).filter(jobs.id == job_id).first()
       if job is None:
           raise HTTPException(status_code=404, detail=f"Job Category with id {job_id} not found or does not belong to the user.")
       else:
           count = db.query(func.count(applications.id)).filter(applications.job_id == job.id).scalar()
           if count > 0:
                # Check if there are applications associated with this job
                raise HTTPException(status_code=400, detail="Cannot delete job because it's already associated with an application.")
           if job.user_id != TheUser.id:
               # Check if the user is not the creator and is not an admin
               raise HTTPException(status_code=403, detail="You do not have permission to delete this job.")
           db.delete(job)
           db.commit()
           return {"detail": "Job deleted successfully"}
    except Exception as e:       
        raise HTTPException(status_code=404, detail=f"Error deleting job category: {str(e)})") 

    