from fastapi import  Depends,Query
from sqlalchemy.orm import Session 
from utils.jobs import getjob 
from models.database import  get_db
from models.jobs import JobStatus
from schemas.jobs.job import ListJobSchema 
from schemas.users.user import User
from utils.general.authentication import get_current_user
from typing import  Optional
from datetime import datetime
from .router import router

@router.get("/getjobbystatus", include_in_schema=True, response_model=list[ListJobSchema])
async def do(status: JobStatus,
                    db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):   
    return getjob.get_job_by_status(status, db)





