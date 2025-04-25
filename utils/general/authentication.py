from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from models.accounts import Users 
from schemas.users.user import User  
from models.database import  get_db
from .dependencies import oauth2_scheme 
import jwt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") 
def get_password_hash(password):
    return pwd_context.hash(password)
def verify_password(plain_password, hashed_password): # plain_password is supplied by user... hashed_password is read from DB
    import hashlib
    plain_password = hashlib.md5(plain_password.strip().encode()).hexdigest() # converts to the form used to store passwords in DB
    hashed_password = get_password_hash(hashed_password) 
            # converts what it read from DB into the form used by the hash engine of this library
    return pwd_context.verify(plain_password, hashed_password)
# Secret key to encode JWT
SECRET_KEY = "This is by Dekun 2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 
from pydantic import BaseModel
class Token(BaseModel):
    access_token: str
    token_type: str 
class TokenData(BaseModel):
    username: Optional[str] = None  
def authenticate_user(db: Session, username: str, password: str):     
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False     
    if not verify_password(password, user.password):        
        return False
    return user 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
'''
def get_current_user():
    pass
'''
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        exp: int = payload.get("exp")  # Get the current expiration time         
        if username is None:
            raise credentials_exception         
        token_data = TokenData(username=username)         
        # Check the remaining time before expiration
        current_time = datetime.utcnow()
        expiration_time = datetime.utcfromtimestamp(exp)
        time_left = expiration_time - current_time      
        # Refresh the token's expiration time if it's about to expire
        if time_left < timedelta(minutes=5):  # You can adjust the threshold
            new_exp = current_time + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            payload.update({"exp": new_exp})
            token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)      
        ThisUser = db.query(Users).filter(Users.username == token_data.username).first()
        if ThisUser is None:
            raise HTTPException(status_code=401, detail=f"User({token_data.username} not valid)")   
        # You can log or return the refreshed token if needed
        return User( 
            id=ThisUser.id, 
            username=ThisUser.username,  
            firstname=ThisUser.firstname,  
            middlename=ThisUser.middlename, 
            lastname=ThisUser.lastname,
            emailAddy=ThisUser.emailAddy, 
            dateCreated=ThisUser.dateTimeCreated
        )  
    except Exception as e:
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"get_current_user: {e}",
        headers={"WWW-Authenticate": "Bearer"},
    ) 
        raise credentials_exception     
 
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=400, detail="Not a valid user")
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user 