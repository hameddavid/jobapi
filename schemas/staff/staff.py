from ..users.user import User 
from pydantic import BaseModel
class Staff(User):    
    designation: str
    department: str
    is_Active: bool
    class Config:
        orm_mode = True   
class StaffAUTH(BaseModel):   
    staff: Staff
    token: str  
    class Config:
        orm_mode = True  