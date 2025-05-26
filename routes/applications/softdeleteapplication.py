from fastapi import  Depends
from sqlalchemy.orm import Session
from utils.application.delete import soft_delete_application
from models.database import  get_db
from schemas.users.user import User
from schemas.general.deletion import SoftDeletion
from utils.general.authentication import user_required_roles
from .router import router

    
@router.delete("/hide_application/", include_in_schema=True, response_model="")          
async def do(app_id: int,delStatus: SoftDeletion,db: Session = Depends(get_db),TheUser: User = Depends(user_required_roles(['admin']))):
   return soft_delete_application(app_id,delStatus,TheUser, db)
