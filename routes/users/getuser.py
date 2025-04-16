from fastapi import APIRouter, Depends, Path 
from sqlalchemy.orm import Session 
from utils.users.getuser import get_user, get_user_by_email, get_users_all
from models.database import  get_db 
from schemas.users.user import User
from schemas.operators.operator import Operator
from utils.general.authentication import get_current_user
from utils.general.dependencies import oauth2_scheme
 
router = APIRouter()
@router.get("/users/me")
async def do(TheUser: User = Depends(get_current_user)):
    return TheUser 
@router.get("/getuser/{username}",
            include_in_schema=True, 
            response_model=User)
async def do(username: str, db: Session = Depends(get_db),TheUser: User = Depends(get_current_user) ):  
    return get_user(username, db)
@router.get("/getuserbyemail/{emailAddy}",
            include_in_schema=True, 
            response_model= User)
async def do(emailAddy: str = Path(..., min_length=5, max_length=45),
                    db: Session = Depends(get_db),TheUser: User = Depends(get_current_user) ):   
    return get_user_by_email(emailAddy, db) 
@router.get("/getusers/",
            include_in_schema=True, 
            response_model= list[User])
async def do(skip: int = 0, limit:int = 100,
                    db: Session = Depends(get_db), TheUser: User = Depends(get_current_user)): 
    return get_users_all(skip, limit, db)
