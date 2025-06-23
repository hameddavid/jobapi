from fastapi import  Depends
from sqlalchemy.orm import Session
from utils.rating.deleteRating import toggle_step_down_rating
from models.database import  get_db
from schemas.users.user import User
from schemas.general.deletion import  SoftDeletion
from utils.general.authentication import user_required_roles
from .router import router

    
@router.patch("/toggle_step_down_rating/", include_in_schema=True, response_model="")          
async def do(rateId: int, delStatus: SoftDeletion , db: Session = Depends(get_db),TheUser: User = Depends(user_required_roles(['admin']))):
   return toggle_step_down_rating(rateId,delStatus,TheUser, db)




   