from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session
from utils.admins.loginadmin import LoginAdmin as fLoginAdmin
from models.database import  get_db
from schemas.admins.admin import  AdminAUTH
from schemas.general.login import LoginAdmin
router = APIRouter()     
@router.post("/loginAdmin/", include_in_schema=True, response_model = AdminAUTH)          
async def do(payload: LoginAdmin = Body(..., embed= True), db: Session = Depends(get_db)):
   return fLoginAdmin(payload, db)
