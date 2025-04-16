from pydantic import BaseModel, EmailStr
from infrastructure.types.fingerstypeatenrol import  FingersTypeAtEnrol
from typing import List 
class FingerprintCreate(BaseModel):
    username: str  #  this or emailAddy must be set...   student account must have been created
    emailAddy:EmailStr  
    fingers: List[FingersTypeAtEnrol]  # =>  [ (thumb,base), (thumb, instance), (inde, base) and (index, instance) ]