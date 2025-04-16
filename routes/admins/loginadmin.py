from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session
from utils.admins.loginadmin import LoginAdmin 
from models.database import  get_db
from schemas.admins.admin import Admin, AdminAUTH
from schemas.general.login import Login 
router = APIRouter()     
@router.post("/loginAdmin/", include_in_schema=True, response_model = AdminAUTH)          
async def do(payload: Login = Body(..., embed= True), db: Session = Depends(get_db)):
   return LoginAdmin(payload, db)
