
from pydantic import BaseModel 
from datetime import datetime
from typing import Optional
from schemas.users.user import User as UserSchema

from pydantic import  ConfigDict

class CreateJobCategorySchema(BaseModel):   
    name: str
    description: Optional[str] = None 
 

class UpdateJobCategorySchema(CreateJobCategorySchema):
    id: int
    deleted: str = 'N'

class GetJobCategorySchema(BaseModel): 
    id: int  
    name: str
    description: str  
    deleted : str = 'N'
    createdBy: UserSchema
    createdAt: datetime
    updatedAt: datetime
    
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True  
    
    
