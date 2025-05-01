from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session 
from utils.users.createuser import  create_user
from models.database import  get_db
from schemas.users.user import User
from schemas.users.usercreate import UserCreate 
router = APIRouter()
@router.post("/createUser/", include_in_schema = False, response_model= User)         # used to create a record for user if none exists before now
async def do(user: UserCreate = Body(..., embed= True), db: Session = Depends(get_db)):
   return create_user(user, db)
