from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session  
from models.database import  get_db 
from schemas.admins.admin import Admin
from schemas.admins.adminupdate import AdminUpdate
from utils.admins.updateadmin import update_admin
from schemas.users.user import User
from utils.general.authentication import get_current_user, user_required_roles
router = APIRouter()     
@router.put("/updateAdmin/", response_model=Admin)         # update user if it exists
async def do(user: AdminUpdate = Body(..., embed= True), db: Session = Depends(get_db),TheUser: User = Depends(user_required_roles(["super_admin"]))):
   return update_admin(user, db)
