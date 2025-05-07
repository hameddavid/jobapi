
from pydantic import BaseModel 
from datetime import datetime

class CreateJobCategorySchema(BaseModel):   
    name: str
    description: str | None = None 
 

class UpdateJobCategorySchema(CreateJobCategorySchema):
    id: int
    deleted: str = 'N'

class GetJobCategorySchema(BaseModel): 
    id: int  
    name: str
    description: str  
    deleted : str = 'N'
    createdBy: int
    createdAt: datetime
    updatedAt: datetime
    
    class Config:
        orm_mode = True  
    
    
