from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session
from utils.staff.loginstaff import LoginStaff as fLoginStaff
from models.database import  get_db
from schemas.staff.staff import  StaffAUTH
from schemas.general.login import LoginStaff
router = APIRouter()     
@router.post("/loginStaff/", include_in_schema=True, response_model = StaffAUTH)          
async def do(payload: LoginStaff = Body(..., embed= True), db: Session = Depends(get_db)):
   return fLoginStaff(payload, db)
