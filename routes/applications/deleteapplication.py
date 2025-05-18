from fastapi import  Depends
from sqlalchemy.orm import Session
from utils.application.delete import delete_application
from models.database import  get_db
from schemas.users.user import User
from utils.general.authentication import get_current_user
from .router import router

    
@router.delete("/deleteapplication/", include_in_schema=True, response_model="")          
async def do(app_id: int, db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):
   return delete_application(app_id,TheUser, db)
