from pydantic import BaseModel, EmailStr 
class SendPassResetLink(BaseModel): 
    emailAddy: EmailStr 
    frontendURL:str  # used by frontend when  
    processor:str  # page or route used by the frontend app   
     
   
     
     