from .router import router
from fastapi import Depends, Body 
from schemas.users.user import User
from sqlalchemy.orm import Session 
from schemas.apps.appschema import GetAppSchema
from models.database import  get_db
from utils.application.getapp import list_my_apps
from utils.general.authentication import get_current_user, user_required_roles

@router.get("/list_my_applications", include_in_schema=True, response_model=list[GetAppSchema])
async def do(skip: int = 0, limit:int = 100,
                    db: Session = Depends(get_db),TheUser: User = Depends(user_required_roles(["student","staff"]))):
    
    return list_my_apps(TheUser,skip,limit, db)