from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session 
from utils.staff.getstaff import get_staff, get_staff_by_email, get_staffs_all
from models.database import  get_db 
from schemas.staff.staff import Staff
from schemas.users.user import User
from utils.general.authentication import get_current_user
router = APIRouter()
@router.get("/getstaff",
            include_in_schema=True, 
            response_model= Staff)
async def do(username: str, db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):   
    return get_staff(username, db)
@router.get("/getstaffbyemail",
            include_in_schema=True, 
            response_model= Staff)
async def do(emailAddy: str, db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):   
    return get_staff_by_email(emailAddy, db) 
@router.get("/getstaffs",
            include_in_schema=True, 
            response_model= list[Staff])
async def do(skip: int = 0, limit:int = 100,
                    db: Session = Depends(get_db),TheUser: User = Depends(get_current_user) ):   
    return get_staffs_all(skip, limit, db)
 

 
