from pydantic import BaseModel 
class JobCreate(BaseModel):   
    title: str
    description: str  
    listed_price: float
     
     