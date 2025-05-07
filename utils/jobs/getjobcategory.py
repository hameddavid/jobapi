from models.jobs import jobCategory as jobCatModel
from schemas.jobs.jobCategorySchema import GetJobCategorySchema 
from schemas.users.user import User as UserSchema
from fastapi import   HTTPException
from sqlalchemy.orm import Session , joinedload

def list_job_cat(skip:int, limit:int, db: Session) -> list[GetJobCategorySchema]:
    try:
        
        catQ = (db.query(jobCatModel)
                .options(
                    joinedload(jobCatModel.user)  # Eagerly load user of category
                )
                .offset(skip).limit(limit).all())
        if catQ is None:
            raise HTTPException(status_code=404, detail=f"Jobs(skip={skip}, limit={limit}) not found")
        lstcats: list[GetJobCategorySchema]= []
        for cat in catQ:
            cat_owner = UserSchema.model_validate(cat.user)
            ThisJob =  GetJobCategorySchema(id=cat.id, name=cat.name, description=cat.description,
                                            deleted=cat.deleted, createdBy=cat_owner,
                                            createdAt=cat.createdAt, updatedAt=cat.updatedAt)
            
            lstcats.append(ThisJob)
        return lstcats
    
    except Exception as e:       
        raise HTTPException(status_code=404, detail=f"Error listing job categories : {str(e)})") 