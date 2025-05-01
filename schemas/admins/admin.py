from ..users.user import User
from pydantic import BaseModel
class Admin(User):  
    is_Active: bool
    class Config:
        orm_mode = True   

class AdminAUTH(BaseModel):   
    admin: Admin
    token: str  
    class Config:
        orm_mode = True   