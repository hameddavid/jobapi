from fastapi import  Depends,Query
from sqlalchemy.orm import Session 
from utils.jobs import getjob 
from models.database import  get_db
from schemas.jobs.job import ListJobSchema 
from schemas.users.user import User
from utils.general.authentication import get_current_user
from typing import  Optional
from datetime import datetime
from pydantic import  Field
from .router import router

@router.get("/getjob", include_in_schema=True, response_model=ListJobSchema)
async def do(job_id: int,
                    db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):   
    return getjob.get_job_by_id(job_id, db)




@router.get("/searchjobs", response_model=list[ListJobSchema])
def search_jobs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1),
    category_id: Optional[int] = None,
    owner_id: Optional[int] = None,
    job_name: Optional[str] = None,
    location: Optional[str] = None,
    job_description: Optional[str] = None,
    date_from: Optional[datetime] = Query(
        default=None,
        description="",
        example="YYYY-MM-DD orYYYY-MM-DDTHH:MM:SS",
    ),
    date_to: Optional[datetime] = Query(
        default=None,
        description="",
        example="YYYY-MM-DD orYYYY-MM-DDTHH:MM:SS",
    ),
):
    return getjob.list_jobs_with_filters(
        db=db,
        skip=skip,
        limit=limit,
        category_id=category_id,
        owner_id=owner_id,
        job_name=job_name,
        location=location,
        job_description=job_description,
        date_from=date_from,
        date_to=date_to,
    )
