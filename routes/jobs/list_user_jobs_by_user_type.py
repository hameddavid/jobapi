from fastapi import  Depends 
from sqlalchemy.orm import Session 
from utils.jobs import getjob 
from models.database import  get_db
from schemas.jobs.job import ListJobSchema 
from schemas.users.user import User, UserType
from utils.general.authentication import user_required_roles
from .router import router

@router.get("/list_jobs_by_user_type", include_in_schema=True, response_model=list[ListJobSchema])
async def do(user_type:UserType, skip: int = 0, limit:int = 100,
                    db: Session = Depends(get_db),TheUser: User = Depends(user_required_roles(["admin"]))):   
    return getjob.get_jobs_by_user_type(user_type,skip, limit, db)


