from ..users.user import User
from pydantic import BaseModel
from typing import Dict
class Admin(User):  
    is_Active: bool
    class Config:
        orm_mode = True   

class AdminAUTH(BaseModel):   
    admin: Admin
    token: Dict[str, str]   
    class Config:
        orm_mode = True   