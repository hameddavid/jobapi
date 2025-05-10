from fastapi import   HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.jobs import jobCategory, jobs




def delete_job_category(cat_id: int,TheUser, db: Session ):  
    
    try:
       cat = db.query(jobCategory).filter(jobCategory.id == cat_id).first()
       if cat is None:
           raise HTTPException(status_code=404, detail=f"Job Category with id {cat_id} not found or does not belong to the user.")
       else:
           count = db.query(func.count(jobs.id)).filter(jobs.job_category_id == cat.id).scalar()
           if count > 0:
                # Check if there are jobs associated with this category
                raise HTTPException(status_code=400, detail="Cannot delete job category because it's already associated with jobs.")
               
           if cat.createdBy != TheUser.id and "admin" not in TheUser.roles:
               # Check if the user is not the creator and is not an admin
               raise HTTPException(status_code=403, detail="You do not have permission to update this job category.")
           db.delete(cat)
           db.commit()
           return {"detail": "Job category deleted successfully"}
    except Exception as e:       
        raise HTTPException(status_code=404, detail=f"Error deleting job category: {str(e)})") 

    