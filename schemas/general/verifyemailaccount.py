from pydantic import BaseModel, EmailStr 
class VerifyEmailAccount(BaseModel): 
    email: EmailStr
    password: str
    eCode:str    
     
   
     
     