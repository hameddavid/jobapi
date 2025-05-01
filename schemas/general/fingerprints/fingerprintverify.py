from pydantic import BaseModel, EmailStr
from infrastructure.types.fingerprintverify import  FingersTypeAtVerify 
from typing import List 
class FingerprintVerify(BaseModel):
    username: str  #  this or emailAddy must be set...   student account must have been created
    emailAddy:EmailStr  
    finger: FingersTypeAtVerify # =>  any [ (thumb,base), (thumb, instance), (inde, base) and (index, instance) ]