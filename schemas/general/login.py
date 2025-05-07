from pydantic import BaseModel, EmailStr 
class Login(BaseModel):      
    username: str   # matric number for UG students
    password:str
    frontendURL:str  # used by frontend to verify user account, eg operator, staff or student account 
    processor:str  # page or route used by the frontend app   


class LoginAdmin(BaseModel):      
    emailAddy: EmailStr   # matric number for UG students
    password:str
    frontendURL:str  # used by frontend to verify user account, eg operator, staff or student account 
    processor:str  # page or route used by the frontend app   

class LoginStaff(BaseModel):      
    emailAddy: EmailStr   # matric number for UG students
    password:str
    frontendURL:str  # used by frontend to verify user account, eg operator, staff or student account 
    processor:str  # page or route used by the frontend app 