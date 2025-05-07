from fastapi import  Depends
from sqlalchemy.orm import Session
from utils.jobs.deletejobcategory import delete_job_category
from models.database import  get_db
from schemas.users.user import User
from utils.general.authentication import get_current_user
from .router import router

    
@router.delete("/deleteJobCategory/", include_in_schema=True, response_model="")          
async def do(jobCatId: int, db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):
   return delete_job_category(jobCatId,TheUser, db)




   