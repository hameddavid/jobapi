from fastapi import   HTTPException
from sqlalchemy.orm import Session
from models.jobs import jobCategory
from schemas.jobs import jobCategorySchema

def create_job_category(jobCat:jobCategorySchema.CreateJobCategorySchema,TheUser, db: Session ):  
    
    try:
        jobCat = jobCategory(
            name = str(jobCat.name).capitalize(),
            description =  str(jobCat.description).capitalize(),
            createdBy = TheUser.id
        )
        db.add(jobCat)
        db.commit()
        db.refresh(jobCat)
        return jobCat
    except Exception as e:       
        raise HTTPException(status_code=404, detail=f"Error creating job category: {str(e)})") 

    