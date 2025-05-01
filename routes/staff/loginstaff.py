from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session
from utils.staff.loginstaff import LoginStaff
from models.database import  get_db
from schemas.staff.staff import Staff, StaffAUTH
from schemas.general.login import Login 
router = APIRouter()     
@router.post("/loginStaff/", include_in_schema=True, response_model = StaffAUTH)          
async def do(payload: Login = Body(..., embed= True), db: Session = Depends(get_db)):
   return LoginStaff(payload, db)
