from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session  
from models.database import  get_db 
from schemas.admins.admin import Admin
from schemas.general.verifyemailaccount import VerifyEmailAccount
from utils.admins.verifyadmin import verify_admin
router = APIRouter()     
@router.patch("/verifyAdmin/", response_model=Admin)         # verifies email account of admin
async def do(payload: VerifyEmailAccount = Body(..., embed= True), db: Session = Depends(get_db)):
   return verify_admin(payload, db)
