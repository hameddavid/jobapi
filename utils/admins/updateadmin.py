from fastapi import   HTTPException
from sqlalchemy.orm import Session 
from sqlalchemy import func
from schemas.admins.adminupdate import AdminUpdate 
from schemas.admins.admin import Admin
def update_admin(admin: AdminUpdate, db: Session ):  
   try:       
    from .getadmin import get_admin_by_email_ver2
    ThisAdmin:Admin =  get_admin_by_email_ver2(admin.emailAddy, db)  #  returns None if email not in DB
    if ThisAdmin is None:
       raise HTTPException(status_code=404, detail=f"Admin(email={admin.emailAddy}) does not exist in DB.") 
    if ThisAdmin.username != admin.username:
        raise HTTPException(status_code=404, detail=f"Admin(username={admin.username}) does not exist in DB.")    
    from models.accounts import  Users
    updateStmt = {"firstname": admin.firstname,
                  "middlename": admin.middlename,
                  "lastname": admin.lastname}
    db.reset() # resets the database session
    db.begin()
    db.query(Users).where(func.trim(func.lower(Users.username)) == admin.username.strip().lower() and
                                        func.trim(func.lower(Users.emailAddy)) == admin.emailAddy.strip().lower()).update(updateStmt)
    db.commit()    
    return Admin(id = ThisAdmin.id, username = ThisAdmin.username,  firstname = admin.firstname,  
                    middlename = admin.middlename, lastname = admin.lastname,emailAddy = ThisAdmin.emailAddy, 
                    dateTimeCreated = ThisAdmin.dateTimeCreated, is_Active=  ThisAdmin.is_Active)     
   except Exception as e:
        db.rollback()
        raise e
    
  