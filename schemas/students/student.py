from ..users.user import User 
from pydantic import BaseModel
class Student(User):    
    programme: str
    level: int  
    is_UG:bool
    is_Active: bool   
    class Config:
        orm_mode = True    

class StudentAUTH(BaseModel):   
    student: Student
    token: str  
    class Config:
        orm_mode = True  