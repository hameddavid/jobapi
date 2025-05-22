from datetime import datetime
from .userbase import UserBase 
from pydantic import  ConfigDict
from enum import Enum
class User(UserBase):    
    dateTimeCreated: datetime
    roles: list[str] = [] 
    id: int
    
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     orm_mode = True    


class UserType(str, Enum):
    STUDENT = "STUDENT"
    STAFF = "STAFF"