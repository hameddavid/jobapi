from ..users.user import User
class Operator(User):    
    machineMacAddress: str
    is_Active: bool
    class Config:
        orm_mode = True    