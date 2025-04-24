from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session
from utils.admins.resetadmin import ResetPasswordAdmin 
from models.database import  get_db
from schemas.admins.admin import Admin
from schemas.general.resetPassword import ResetPassword 
router = APIRouter()     
@router.patch("/resetAdminPassword/", include_in_schema=True, response_model=Admin)          
async def do(payload: ResetPassword = Body(..., embed= True), db: Session = Depends(get_db)):
   return ResetPasswordAdmin(payload, db)
