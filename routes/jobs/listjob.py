from fastapi import  Depends 
from sqlalchemy.orm import Session 
from utils.jobs import getjob 
from models.database import  get_db
from schemas.jobs.job import ListJobSchema 
from schemas.users.user import User
from utils.general.authentication import get_current_user
from .router import router

@router.get("/listjobs", include_in_schema=True, response_model=list[ListJobSchema])
async def do(skip: int = 0, limit:int = 100,
                    db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):   
    return getjob.list_jobs(skip, limit, db)


