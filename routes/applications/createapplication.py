from .router import router
from fastapi import Depends ,status
from schemas.users.user import User
from sqlalchemy.orm import Session 
from schemas.apps.appschema import CreateAppSchema,CreateAppRespSchema
from models.database import  get_db
from utils.application.create import create_app
from utils.general.authentication import  user_required_roles







@router.post("/createapplications", include_in_schema=True, response_model=CreateAppRespSchema, status_code=status.HTTP_201_CREATED)
async def do(jobApp: CreateAppSchema = Depends(), db: Session = Depends(get_db),
              TheUser: User = Depends(user_required_roles(["student","staff"]))):
    
    return await create_app(jobApp,TheUser, db)



