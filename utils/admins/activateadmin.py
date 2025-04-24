from fastapi import   HTTPException
from sqlalchemy.orm import Session
from schemas.admins.admin import Admin  
from models.accounts import Users, Admins   
def activate_admin(emailAddy: str, bActivate:bool, db: Session):
    try:
        # Find the user by email address
        user = db.query(Users).filter(Users.emailAddy == emailAddy).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User (email = {emailAddy}) not found")         
        # Find the admin by user ID
        ThisAdmin = db.query(Admins).filter(Admins.user_id == user.id).first()
        if not ThisAdmin:
            raise HTTPException(status_code=404, detail=f"Admin (email = {emailAddy}) not found")  
        if user.isVerifiedEmail == False:
            raise HTTPException(status_code=404, detail=f"Admin (activate account): Check inbox {emailAddy}to verify (user) account")          
        # Update the is_active field
        ThisAdmin.is_Active = 0
        if bActivate:
            ThisAdmin.is_Active = 1
        db.commit()
        db.refresh(ThisAdmin)
        return Admin(id = ThisAdmin.id, username = user.username,  firstname = user.firstname,  
                    middlename = user.middlename, lastname = user.lastname,emailAddy = user.emailAddy, 
                    dateCreated = ThisAdmin.dateTimeCreated, is_Active=  ThisAdmin.is_Active)   
    except Exception as e:
        db.rollback()
        raise e