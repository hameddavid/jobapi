from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session  
from models.database import  get_db 
from schemas.admins.admin import Admin
from utils.admins.activateadmin import  activate_admin
from schemas.users.user import User
from utils.general.authentication import get_current_user
router = APIRouter()     
@router.put("/activateAdmin/", response_model=Admin)         # only super admin can activate other admins
async def do(emailAddy: str, activate:bool, db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):
   return activate_admin(emailAddy,activate, db)
