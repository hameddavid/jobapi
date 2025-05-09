from fastapi import  Depends, Body 
from sqlalchemy.orm import Session
from utils.jobs.updatejobcategory import   update_job_category
from models.database import  get_db
from schemas.jobs import jobCategorySchema
from schemas.users.user import User
from utils.general.authentication import get_current_user
from .router import router
    
@router.patch("/updateJobCategory/", include_in_schema=True, response_model=jobCategorySchema.GetJobCategorySchema)          
async def do(jobCat: jobCategorySchema.UpdateJobCategorySchema = Body(..., embed= True), db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):
   return update_job_category(jobCat,TheUser, db)




   