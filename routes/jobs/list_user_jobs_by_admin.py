from fastapi import  Depends 
from sqlalchemy.orm import Session 
from utils.jobs import getjob 
from models.database import  get_db
from schemas.jobs.job import ListJobSchema 
from schemas.users.user import User
from utils.general.authentication import user_required_roles
from .router import router

@router.get("/list_user_jobs_by_admin", include_in_schema=True, response_model=list[ListJobSchema])
async def do(user_id, skip: int = 0, limit:int = 100,
                    db: Session = Depends(get_db),TheUser: User = Depends(user_required_roles(["admin"]))):   
    return getjob.list_user_jobs_by_admin(user_id,skip, limit, db)


