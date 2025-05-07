from fastapi import   HTTPException
from sqlalchemy.orm import Session
from models.jobs import jobCategory
from schemas.jobs import jobCategorySchema
from schemas.jobs.jobCategorySchema import GetJobCategorySchema
from schemas.users.user import User as UserSchema

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
        cat_owner = UserSchema.model_validate(jobCat.user)
        return GetJobCategorySchema(id = jobCat.id, name = jobCat.name, description = jobCat.description,
                deleted = jobCat.deleted, createdBy = cat_owner,
                createdAt = jobCat.createdAt, updatedAt = jobCat.updatedAt)
    except Exception as e:       
        raise HTTPException(status_code=404, detail=f"Error creating job category: {str(e)})") 
    

    