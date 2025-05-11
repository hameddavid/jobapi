from models.jobs import jobCategory as jobCatModel
from schemas.jobs.jobCategorySchema import GetJobCategorySchema 
from schemas.users.user import User as UserSchema
from fastapi import   HTTPException
from sqlalchemy import func
from typing import Optional
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
    
    
    
    


def search_job_categories(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> list[GetJobCategorySchema]:
    try:
        # Base query with eager loading
        query = (
            db.query(jobCatModel)
            .options(
                joinedload(jobCatModel.user)  # Eagerly load user of category
            )
        )

        # Apply filters dynamically
        if name:
            query = query.filter(func.lower(jobCatModel.name).contains(name.lower()))
        if description:
            query = query.filter(func.lower(jobCatModel.description).contains(description.lower()))

        # Apply pagination
        categories = query.offset(skip).limit(limit).all()

        if not categories:
            raise HTTPException(status_code=404, detail="No job categories found with the given filters")

        # Serialize the results
        lstcats: list[GetJobCategorySchema] = []
        for cat in categories:
            cat_owner = UserSchema.model_validate(cat.user)
            ThisJob = GetJobCategorySchema(
                id=cat.id,
                name=cat.name,
                description=cat.description,
                deleted=cat.deleted,
                createdBy=cat_owner,
                createdAt=cat.createdAt,
                updatedAt=cat.updatedAt,
            )
            lstcats.append(ThisJob)

        return lstcats

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching job categories: {str(e)}")