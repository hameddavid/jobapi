from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session
from utils.admins.sendpassresetlink import SendLink 
from models.database import  get_db
from schemas.admins.admin import Admin
from schemas.general.sendpasswordresetlink import SendPassResetLink 
router = APIRouter()     
@router.post("/sendPassResetLinkAdmin/", include_in_schema=True, response_model=Admin)          
async def do(payload: SendPassResetLink = Body(..., embed= True), db: Session = Depends(get_db)):
   return SendLink(payload, db)
