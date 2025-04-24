from pydantic import BaseModel, EmailStr 
class UserBase(BaseModel):      
    username: str 
    emailAddy:EmailStr
    firstname:str
    middlename:str
    lastname:str