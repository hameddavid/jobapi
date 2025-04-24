from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session
from utils.staff.createstaff import  create_staff
from models.database import  get_db
from  schemas.staff.staff import Staff
from schemas.staff.staffcreate import StaffCreate 
router = APIRouter()     
@router.post("/createStaff/", include_in_schema=True, response_model=Staff)          
async def do(user: StaffCreate = Body(..., embed= True), db: Session = Depends(get_db)):
   return create_staff(user, db)
