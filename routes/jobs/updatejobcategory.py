from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session
from utils.jobs.jobCategory import create_job_category
from models.database import  get_db
from schemas.jobs import jobCategorySchema

router = APIRouter()     

@router.post("/updateJobCategory/", include_in_schema=True)         #, response_model=jobCategorySchema.GetJobCategorySchema 
async def update(id:int, jobCat: jobCategorySchema.CreateJobCategorySchema = Body(..., embed= True), db: Session = Depends(get_db)):
   return create_job_category(jobCat, db)

