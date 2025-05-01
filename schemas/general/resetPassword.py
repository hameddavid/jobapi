from pydantic import BaseModel, EmailStr 
class ResetPassword(BaseModel): 
    emailAddy: EmailStr 
    password:str
    passwordConfirmed:str
    eCode:str # encoded string is retrieved from the link that's sent to User's inbox
   
     
     