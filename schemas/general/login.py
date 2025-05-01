from pydantic import BaseModel, EmailStr 
class Login(BaseModel):      
    emailAddy: EmailStr 
    password:str
    frontendURL:str  # used by frontend to verify user account, eg operator, staff or student account 
    processor:str  # page or route used by the frontend app   