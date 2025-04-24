from datetime import datetime
from .userbase import UserBase 
class User(UserBase):    
    dateCreated: datetime
    id: int
    class Config:
        orm_mode = True    