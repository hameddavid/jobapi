from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session 
from utils.admins.getadmin import get_admin, get_admin_by_email, get_admins_all
from models.database import  get_db 
from schemas.admins.admin import Admin
from schemas.users.user import User
from utils.general.authentication import get_current_user
router = APIRouter()
@router.get("/getadmin",
            include_in_schema=True, 
            response_model= Admin)
async def do(username: str, db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):   
    return get_admin(username, db)
@router.get("/getadminbyemail",
            include_in_schema=True, 
            response_model= Admin)
async def do(emailAddy: str, db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):   
    return get_admin_by_email(emailAddy, db) 
@router.get("/getadmins",
            include_in_schema=True, 
            response_model= list[Admin])
async def do(skip: int = 0, limit:int = 100,
                    db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):   
    return get_admins_all(skip, limit, db)