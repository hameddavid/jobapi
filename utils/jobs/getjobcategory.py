from models.jobs import jobCategory as jobCatModel
from schemas.jobs.jobCategorySchema import GetJobCategorySchema 
from schemas.users.user import User as UserSchema
from fastapi import   HTTPException
from sqlalchemy.orm import Session 

def list_job_cat(skip:int, limit:int, db: Session):
    try:
        
        catQ = db.query(jobCatModel).offset(skip).limit(limit).all()
        if catQ is None:
            raise HTTPException(status_code=404, detail=f"Jobs(skip={skip}, limit={limit}) not found")
        lstcats: list[GetJobCategorySchema]= []
        for cat in catQ:
            
            cat_owner = UserSchema(id = cat.user.id, username = cat.user.username, emailAddy = cat.user.emailAddy,
                    firstname = cat.user.firstname, lastname = cat.user.lastname,
                    middlename = cat.user.middlename, dateCreated = cat.user.dateTimeCreated,) 
            
            ThisJob =  GetJobCategorySchema(id=cat.id, name=cat.name, description=cat.description,
                                            deleted=cat.deleted, createdBy=cat_owner,
                                            createdAt=cat.createdAt, updatedAt=cat.updatedAt)
            
            lstcats.append(ThisJob)
        if not lstcats:
            raise HTTPException(status_code=404, detail=f"Jobs(skip={skip}, limit={limit}) not found")
        return lstcats
    except Exception as e:       
        raise HTTPException(status_code=404, detail=f"Error listing job categories : {str(e)})") 