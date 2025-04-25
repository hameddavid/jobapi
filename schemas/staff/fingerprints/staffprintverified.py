from ...users.user import User 
class StaffPrintVerified(User):    
    designation: str
    department: str  
    is_Active: bool   
    finger: str
    is_match: bool
    match_score_base: float
    match_score_instance: float
    matcher: str  # base or instance used to match from db
    class Config:
        orm_mode = True    