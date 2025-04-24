from ..users.userbase import UserBase 
class StudentCreate(UserBase):   
    password:str
    programme: str
    level: int
    is_UG:bool
     
     