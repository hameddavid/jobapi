from pydantic import BaseModel
class OtherApp(BaseModel): 
    id: int 
    shortname:str
    description: str
    callback:str  