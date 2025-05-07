from models.jobs import jobCategory as jobCatModel
from schemas.jobs.jobCategorySchema import GetJobCategorySchema 
from fastapi import   HTTPException
from sqlalchemy.orm import Session 

def list_job_cat(skip:int, limit:int, db: Session):
    catQ = db.query(jobCatModel).offset(skip).limit(limit).all()
    if catQ is None:
        raise HTTPException(status_code=404, detail=f"Jobs(skip={skip}, limit={limit}) not found")
    lstcats: list[GetJobCategorySchema]= []
    for cat in catQ:
        ThisJob =  GetJobCategorySchema(id=cat.id, name=cat.name, description=cat.description,
                                        deleted=cat.deleted, createdBy=cat.createdBy,
                                        createdAt=cat.createdAt, updatedAt=cat.updatedAt)
        # ThisJob =  GetJobCategorySchema.from_orm(cat)
        lstcats.append(ThisJob)
    if not lstcats:
        raise HTTPException(status_code=404, detail=f"Jobs(skip={skip}, limit={limit}) not found")
    return lstcats
