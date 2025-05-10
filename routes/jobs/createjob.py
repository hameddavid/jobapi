from fastapi import Depends, Body 
from sqlalchemy.orm import Session 
from utils.jobs.createjob import   create_job
from models.database import  get_db
from schemas.jobs.job import Job
from schemas.jobs.job import JobCreate 
from schemas.users.user import User
from utils.general.authentication import get_current_user, user_required_roles
from .router import router   
@router.post("/createJob/", include_in_schema=True, response_model=Job)          
async def do(thisJob: JobCreate = Body(..., embed= True), db: Session = Depends(get_db),
              TheUser: User = Depends(user_required_roles(["student","staff"]))):
   return create_job(thisJob,TheUser, db)
