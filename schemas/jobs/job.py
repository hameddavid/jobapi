from pydantic import BaseModel, ConfigDict,Field
from fastapi import UploadFile, File, Form
from datetime import datetime
from models.jobs import JobStatus

from schemas.users.user import User
from schemas.jobs.jobCategorySchema import GetJobCategorySchema
class Owner:
    username: str
    emailAddy: str
    
class Job(BaseModel): 
    id: int  
    title: str
    description: str  
    location: str
    listed_price: float
    status:JobStatus
    doc_1: str
    user_id:  int    #   he posted the job
    job_category_id: int
    dateTimeCreated: datetime
    deleted: str = 'N'
    class Config:
        orm_mode = True  


class JobCreate(BaseModel):   
    title: str
    description: str  
    location: str
    keywords: str
    listed_price: float
    doc_1: UploadFile = File(..., description="Your resume document (PDF, DOCX, jpeg.)"),
    cat_id: int
     

class JobUpdate(JobCreate):
    id: int
    status: JobStatus
    deleted: str = 'N'
    
class ListJobSchema(BaseModel):
    id: int  
    title: str
    description: str  
    location: str
    listed_price: float
    status:JobStatus
    owner:  User    #   he posted the job
    category: GetJobCategorySchema
    dateTimeCreated: datetime
    deleted: str = 'N'
    
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True
    
    
class SimpleJobSchema(BaseModel):
    id: int  
    title: str
    description: str  
    location: str
    listed_price: float
    status:JobStatus
    dateTimeCreated: datetime
    deleted: str = 'N'
    
    model_config = ConfigDict(from_attributes=True)