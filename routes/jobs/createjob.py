from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session 
from utils.jobs.createjob import   create_job
from models.database import  get_db
from schemas.jobs.job import Job
from schemas.jobs.jobcreate import JobCreate 
from schemas.users.user import User
from utils.general.authentication import get_current_user
router = APIRouter()     
@router.post("/createJob/", include_in_schema=True, response_model=Job)          
async def do(thisJob: JobCreate = Body(..., embed= True), db: Session = Depends(get_db),
              TheUser: User = Depends(get_current_user)):
   return create_job(TheUser,thisJob, db)
