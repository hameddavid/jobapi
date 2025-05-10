
import sys
from fastapi import APIRouter, Depends, Body, HTTPException
router = APIRouter()
from sqlalchemy.orm import Session 
from utils.users.createuser import  create_user
from models.database import  get_db
from schemas.users.user import User
from utils.general.authentication import assign_roles_and_create_token
from schemas.users.usercreate import UserCreate 
from  utils.general.authentication import  authenticate_user
from fastapi.security import OAuth2PasswordRequestForm
from utils.general.authentication import  get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from utils.general.authentication import Token, timedelta 
from pydantic import BaseModel
class OAuth2CustomRequest(BaseModel):
    username: str
    password: str

@router.post("/signInUser", response_model=Token)
async def do(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    message = "Endpoint  not yet implemented - '{}' '{}' ".format(form_data.username,form_data.password)
    '''
    raise HTTPException(
            status_code=501,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    '''
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return assign_roles_and_create_token(user, db )
       
