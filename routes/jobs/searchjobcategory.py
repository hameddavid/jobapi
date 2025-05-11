from fastapi import Depends, Body,Query
from typing import  Optional
from sqlalchemy.orm import Session
from utils.jobs.getjobcategory import search_job_categories
from models.database import  get_db
from schemas.jobs import jobCategorySchema
from schemas.users.user import User
from utils.general.authentication import get_current_user
from .router import router  
    


@router.get("/job-categories/search", response_model=list[jobCategorySchema.GetJobCategorySchema])
def search_categories(
    db: Session = Depends(get_db),
    TheUser: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    name: Optional[str] = None,
    description: Optional[str] = None,
):
    return search_job_categories(
        db=db,
        skip=skip,
        limit=limit,
        name=name,
        description=description,
    )