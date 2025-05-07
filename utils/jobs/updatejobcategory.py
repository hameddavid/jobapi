from fastapi import   HTTPException
from sqlalchemy.orm import Session
from models.jobs import jobCategory
from schemas.jobs import jobCategorySchema
from schemas.jobs.jobCategorySchema import GetJobCategorySchema
from schemas.users.user import User as UserSchema

def update_job_category(jobCat:jobCategorySchema.UpdateJobCategorySchema,TheUser, db: Session ):  
    
    try:
       cat = db.query(jobCategory).filter(jobCategory.id == jobCat.id).first()
       if cat is None:
           raise HTTPException(status_code=404, detail=f"Job Category with id {jobCat.id} not found or does not belong to the user.")
       else:
           if cat.createdBy != TheUser.id :     #and TheUser.role != 'admin'
               # Check if the user is not the creator and is not an admin
               raise HTTPException(status_code=403, detail="You do not have permission to update this job category.")
           cat.name = jobCat.name
           cat.description = jobCat.description
           cat.deleted = jobCat.deleted
           db.commit()
           db.refresh(cat)
           cat_owner = UserSchema(id = cat.user.id, username = cat.user.username, emailAddy = cat.user.emailAddy,
                firstname = cat.user.firstname, lastname = cat.user.lastname,
                middlename = cat.user.middlename, dateCreated = cat.user.dateTimeCreated,) 
           return GetJobCategorySchema(id = cat.id, name = cat.name, description = cat.description,
                deleted = cat.deleted, createdBy = cat_owner,
                createdAt = cat.createdAt, updatedAt = cat.updatedAt)
          
    except Exception as e:       
        raise HTTPException(status_code=404, detail=f"Error updating job category: {str(e)})") 

    