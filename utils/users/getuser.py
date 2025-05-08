from fastapi import   HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.accounts import  Users
from schemas.users.user import User 
def get_user(username: str, db: Session ):    
    Thisuser = db.query(Users).filter(func.trim(func.lower(Users.username)) == username.strip().lower()).first()
    if Thisuser:      
        return User( id= Thisuser.id,username = Thisuser.username,  firstname = Thisuser.firstname,  
                 middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                   dateTimeCreated = Thisuser.dateTimeCreated  )    
    raise HTTPException(status_code=404, detail=f"User(username={username}) not found")     
def get_user_by_email(emailAddy: str, db: Session ):    
    Thisuser = db.query(Users).filter(func.trim(func.lower(Users.emailAddy)) == emailAddy.strip().lower()).first()
    if Thisuser:
        return User( id= Thisuser.id, username = Thisuser.username,  firstname = Thisuser.firstname,  
                 middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                   dateTimeCreated = Thisuser.dateTimeCreated ) 
    raise HTTPException(status_code=404, detail=f"User(email={emailAddy}) not found")
def get_user_ver2(username: str, db: Session ):    
    Thisuser = db.query(Users).filter(func.trim(func.lower(Users.username)) == username.strip().lower()).first()
    if Thisuser:      
        return User(id= Thisuser.id, username = Thisuser.username,  firstname = Thisuser.firstname,  
                 middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                   dateTimeCreated = Thisuser.dateTimeCreated)  
    return None
def get_user_by_email_ver2(emailAddy: str, db: Session):    
    Thisuser = db.query(Users).filter(func.trim(func.lower(Users.emailAddy)) == emailAddy.strip().lower()).first()
    if Thisuser:
        return User( id = Thisuser.id, username = Thisuser.username,  firstname = Thisuser.firstname,  
                 middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                   dateTimeCreated = Thisuser.dateTimeCreated)
    return None    
def get_users_all(skip:int, limit:int, db: Session ): 
    ''' 
    from main import exported_vars
    block_locks = exported_vars['shared_block_locks']  
    print(block_locks)
    '''
    users = db.query(Users).offset(skip).limit(limit).all()
    if users is None:
        raise HTTPException(status_code=404, detail=f"Users(skip={skip}, limit={limit}) not found")  
    lstUsers: list[User]= []
    for user in users:     
        lstUsers.append(get_user(user.username, db))
    if not lstUsers: # if list is empty
        raise HTTPException(status_code=404, detail=f"Users(skip={skip}, limit={limit}) not found")  
    return lstUsers