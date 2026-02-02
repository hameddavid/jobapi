from .router import router
from fastapi import Depends, Body 
from schemas.users.user import User
from sqlalchemy.orm import Session 
from schemas.apps.appschema import UpdateAppSchema,CreateAppRespSchema
from models.applications import AppStatus
from models.database import  get_db
from utils.application.update import update_app,update_app_status_by_owner_or_admin
from utils.general.authentication import get_current_user, user_required_roles

@router.patch("/updateapplications", include_in_schema=True, response_model=CreateAppRespSchema)
async def do(jobApp: UpdateAppSchema= Body(..., embed= True), db: Session = Depends(get_db),
              TheUser: User = Depends(user_required_roles(["student","staff"]))):
    
    return update_app(jobApp,TheUser, db)


@router.patch("/updateapplicationstatusbyowneroradmin", include_in_schema=True, response_model=CreateAppRespSchema)
async def do(appId: int, newStatus: AppStatus, db: Session = Depends(get_db),
              TheUser: User = Depends(user_required_roles(["student","staff","admin"]))):
    
    return update_app_status_by_owner_or_admin(appId,newStatus,TheUser, db)

