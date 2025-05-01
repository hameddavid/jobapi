from pydantic import BaseModel 
from datetime import datetime
class Owner:
    username: str
    emailAddy: str
class Job(BaseModel):   
    title: str
    description: str  
    listed_price: float
    status:str
    owner:  str    #   he posted the job
    dateCreated: datetime
    class Config:
        orm_mode = True  

