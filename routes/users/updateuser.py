from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session  
from models.database import  get_db 
from schemas.users.userupdate import  UserUpdate 
from utils.users.updateuser import update_user
from schemas.users.user import User
from utils.general.authentication import get_current_user
router = APIRouter()     
@router.put("/updateUser/")         # update user if it exists
async def do(user: UserUpdate = Body(..., embed= True), db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):
   return update_user(user, db)
