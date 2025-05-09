from datetime import datetime
from .userbase import UserBase 
from pydantic import  ConfigDict
class User(UserBase):    
    dateTimeCreated: datetime
    roles: list[str] = [] 
    id: int
    
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True    