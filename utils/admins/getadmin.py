from fastapi import   HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.accounts import Users, Admins 
from schemas.admins.admin import Admin
 
def get_admin(username: str, db: Session ): 
    queryResult = db.query(Users, Admins).join(Admins, Users.id == Admins.user_id)
    ThisUserAndAdmin = queryResult.filter(func.trim(func.lower(Users.username)) == username.strip().lower()).first()
    if ThisUserAndAdmin is None :
        raise HTTPException(status_code=404, detail = f"Admin(username={username}) not found")    
    Thisuser, ThisAdmin=  ThisUserAndAdmin  # unpacks     
    return Admin(id = ThisAdmin.id,username = Thisuser.username,  firstname = Thisuser.firstname,  
                middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                dateCreated = ThisAdmin.dateTimeCreated, is_Active= ThisAdmin.is_Active)       
def get_admin_by_email(emailAddy: str, db: Session ):    
    queryResult = db.query(Users, Admins).join(Admins, Users.id == Admins.user_id)
    ThisUserAndAdmin= queryResult.filter(func.trim(func.lower(Users.emailAddy)) == emailAddy.strip().lower()).first()
    if ThisUserAndAdmin is None :
        raise HTTPException(status_code=404, detail = f"Admin(emailAddy={emailAddy}) not found")    
    Thisuser, ThisAdmin=  ThisUserAndAdmin  # unpacks     
    return Admin(id = ThisAdmin.id,username = Thisuser.username,  firstname = Thisuser.firstname,  
                middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                dateCreated = ThisAdmin.dateTimeCreated, is_Active= ThisAdmin.is_Active) 
def get_admin_ver2(username: str, db: Session ):    
    queryResult = db.query(Users, Admins).join(Admins, Users.id == Admins.user_id)
    ThisUserAndAdmin = queryResult.filter(func.trim(func.lower(Users.username)) == username.strip().lower()).first()
    if ThisUserAndAdmin is None :
         return ThisUserAndAdmin   
    Thisuser, ThisAdmin=  ThisUserAndAdmin  # unpacks     
    return Admin(id = ThisAdmin.id,username = Thisuser.username,  firstname = Thisuser.firstname,  
                middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                dateCreated = ThisAdmin.dateTimeCreated,  is_Active= ThisAdmin.is_Active) 
def get_admin_by_email_ver2(emailAddy: str, db: Session ):  
    queryResult = db.query(Users, Admins).join(Admins, Users.id == Admins.user_id)
    ThisUserAndAdmin = queryResult.filter(func.trim(func.lower(Users.emailAddy)) == emailAddy.strip().lower()).first()
    if ThisUserAndAdmin is None :
        return ThisUserAndAdmin
    Thisuser, ThisAdmin=  ThisUserAndAdmin  # unpacks     
    return Admin(id = ThisAdmin.id,username = Thisuser.username,  firstname = Thisuser.firstname,  
                middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                dateCreated = ThisAdmin.dateTimeCreated,   is_Active= ThisAdmin.is_Active)
def get_admins_all(skip:int, limit:int, db: Session ): 
    admins = db.query(Admins).offset(skip).limit(limit).all()
    if admins is None:
        raise HTTPException(status_code=404, detail=f"Admins(skip={skip}, limit={limit}) not found")  
    lstAdmins: list[Admin]= []
    for admin in admins:    
        ThisAdmin =  Admin(id = admin.id, username = admin.user.username, firstname = admin.user.firstname,  
                middlename = admin.user.middlename, lastname = admin.user.lastname,emailAddy = admin.user.emailAddy, 
                dateCreated = admin.dateTimeCreated, is_Active= admin.is_Active)       
        lstAdmins.append(ThisAdmin)
    if not lstAdmins: # if list is empty
        raise HTTPException(status_code=404, detail=f"Admins(skip={skip}, limit={limit}) not found")  
    return lstAdmins 