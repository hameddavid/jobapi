from fastapi import  Depends, Body 
from sqlalchemy.orm import Session 
from utils.jobs.updatejob import   update_job
from models.database import  get_db
from schemas.jobs.job import Job , JobUpdate
from schemas.users.user import User
from utils.general.authentication import get_current_user
from .router import router

   
@router.patch("/updateJob/", include_in_schema=True, response_model=Job)          
async def do(thisJob: JobUpdate = Body(..., embed= True), db: Session = Depends(get_db),
              TheUser: User = Depends(get_current_user)):
   return update_job(thisJob,TheUser, db)
