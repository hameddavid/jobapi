from fastapi import  Depends,Query
from sqlalchemy.orm import Session 
from utils.jobs.searchjob import search_job
from models.database import  get_db
from schemas.jobs.job import ListJobSchema 
from schemas.users.user import User
from utils.general.authentication import get_current_user
from .router import router



@router.get("/search_job_full_text", include_in_schema=True, response_model="")
def do(q: str = Query(..., min_length=5),
                    db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):  
 
    return search_job(q, db)