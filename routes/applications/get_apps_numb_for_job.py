from .router import router
from fastapi import Depends 
from schemas.users.user import User
from sqlalchemy.orm import Session 
from schemas.apps.appschema import GetAppSchema
from models.database import  get_db
from utils.application.getapp import get_apps_numb_for_job
from utils.general.authentication import get_current_user

@router.get("/get_apps_numb_for_job", include_in_schema=True, response_model=int)
async def do(job_id: int,
                    db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):
    
    return get_apps_numb_for_job(job_id, db)