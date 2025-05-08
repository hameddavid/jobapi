from fastapi import   HTTPException
from sqlalchemy.orm import Session 
from sqlalchemy import func
from schemas.users.userupdate import UserUpdate
from schemas.users.user import User 
def update_user(user: UserUpdate, db: Session ):  
   try:       
    from .getuser import get_user_by_email
    Thisuser:User =  get_user_by_email(user.emailAddy, db)  # raises exception if user's email does not exist in DB    
    if Thisuser.username != user.username:
        raise HTTPException(status_code=404, detail=f"User(username={user.username}) does not exist in DB.")
    Thisuser.firstname = user.firstname   
    from models.accounts import  Users
    updateStmt = {"firstname": user.firstname,
                  "middlename": user.middlename,
                  "lastname": user.lastname}
    db.reset() # resets the database session
    db.begin()
    db.query(Users).where(func.trim(func.lower(Users.username)) == user.username.strip().lower() and
                                        func.trim(func.lower(User.emailAddy))== user.emailAddy.strip().lower()).update(updateStmt)  
    db.commit()    
    return User( id = Thisuser.id, username = Thisuser.username,  firstname = Thisuser.firstname,  
                  middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                    dateTimeCreated = Thisuser.dateTimeCreated )     
   except Exception as e:
        db.rollback()
        raise e
    
  