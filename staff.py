from ..users.user import User 
from pydantic import BaseModel
from typing import List

class Staff(User):    
    designation: str
    department: str
    is_Active: bool
    class Config:
        orm_mode = True   
class StaffAUTH(BaseModel):   
    staff: Staff
    token: dict  
    class Config:
        orm_mode = True  