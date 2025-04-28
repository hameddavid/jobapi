from pydantic import BaseModel 

class CreateJobCategorySchema(BaseModel):   
    name: str
    description: str  



class GetJobCategorySchema(BaseModel): 
    id: int  
    name: str
    description: str  
    deleted : bool = False
    createdBy: str
    createdAt: str
    updatedAt: str
    
  