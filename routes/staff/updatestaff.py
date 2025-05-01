from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session  
from models.database import  get_db 
from schemas.staff.staff import Staff
from schemas.staff.staffupdate import  StaffUpdate 
from utils.staff.updatestaff import update_staff
from schemas.users.user import User
from utils.general.authentication import get_current_user
router = APIRouter()     
@router.put("/updateStaff/", response_model=Staff)         # update staff if it exists
async def do(user: StaffUpdate = Body(..., embed= True), db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):
   return update_staff(user, db)
