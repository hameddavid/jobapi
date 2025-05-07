from pydantic import BaseModel 
from datetime import datetime

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
    status:int
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
    listed_price: float
    cat_id: int
     

class JobUpdate(JobCreate):
    id: int
    status: int
    deleted: str = 'N'
    
class ListJobSchema(BaseModel):
    id: int  
    title: str
    description: str  
    location: str
    listed_price: float
    status:int
    owner:  User    #   he posted the job
    category: GetJobCategorySchema
    dateTimeCreated: datetime
    deleted: str = 'N'
    class Config:
        orm_mode = True