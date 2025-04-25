from .userbase import UserBase 
class UserCreate(UserBase):  
    password:str
    frontendurl: str  # when email verification is sent to inbox, this url is where user goes to confirm account
    processor:str  # page or route used by frontend app to verify account
     
     