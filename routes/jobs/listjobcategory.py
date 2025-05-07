from fastapi import Depends, Body 
from sqlalchemy.orm import Session
from utils.jobs import getjobcategory
from models.database import  get_db
from schemas.jobs import jobCategorySchema
from schemas.users.user import User
from utils.general.authentication import get_current_user
from .router import router  

@router.get("/listjobcategory", include_in_schema=True, response_model=list[jobCategorySchema.GetJobCategorySchema])
async def do(skip: int = 0, limit:int = 100,
                    db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):   
    return getjobcategory.list_job_cat(skip, limit, db)


