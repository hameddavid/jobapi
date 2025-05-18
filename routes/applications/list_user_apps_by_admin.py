from .router import router
from fastapi import Depends 
from schemas.users.user import User
from sqlalchemy.orm import Session 
from schemas.apps.appschema import GetAppSchema
from models.database import  get_db
from utils.application.getapp import list_user_apps_by_admin
from utils.general.authentication import get_current_user, user_required_roles

@router.get("/list_user_apps_by_admin", include_in_schema=True, response_model=list[GetAppSchema])
async def do(user_id: int,skip: int = 0, limit:int = 100,
                    db: Session = Depends(get_db),TheUser: User = Depends(user_required_roles(["admin"]))):
    
    return list_user_apps_by_admin(user_id,skip,limit, db)