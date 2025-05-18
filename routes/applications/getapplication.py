from .router import router
from fastapi import Depends 
from schemas.users.user import User
from sqlalchemy.orm import Session 
from schemas.apps.appschema import GetAppSchema
from models.database import  get_db
from utils.application.getapp import get_app_by_id
from utils.general.authentication import get_current_user, user_required_roles

@router.get("/get_application", include_in_schema=True, response_model=GetAppSchema)
async def do(app_id: int,
                    db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):
    
    return get_app_by_id(app_id,TheUser, db)