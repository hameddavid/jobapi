from fastapi import   HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.accounts import Users, Staff as Staffs 
from schemas.staff.staff import Staff
 
def get_staff(username: str, db: Session ) -> Staff: 
    queryResult = db.query(Users, Staffs).join(Staffs, Users.id == Staffs.user_id)
    ThisUserAndStaff = queryResult.filter(func.trim(func.lower(Users.username)) == username.strip().lower()).first()
    if ThisUserAndStaff is None :
        raise HTTPException(status_code=404, detail = f"Staff(username={username}) not found")    
    Thisuser, ThisStaff=  ThisUserAndStaff  # unpacks     
    return Staff(id = ThisStaff.id,username = Thisuser.username,  firstname = Thisuser.firstname,  
                middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                dateTimeCreated = ThisStaff.dateTimeCreated, designation=  ThisStaff.designation, 
                department= ThisStaff.department, is_Active= ThisStaff.is_Active)    
def get_staff_by_email(emailAddy: str, db: Session ) -> Staff:    
    queryResult = db.query(Users, Staffs).join(Staffs, Users.id == Staffs.user_id)
    ThisUserAndStaff = queryResult.filter(func.trim(func.lower(Users.emailAddy)) == emailAddy.strip().lower()).first()
    if ThisUserAndStaff is None :
        raise HTTPException(status_code=404, detail = f"Staff(emailAddy={emailAddy}) not found")    
    Thisuser, ThisStaff=  ThisUserAndStaff  # unpacks     
    return Staff(id = ThisStaff.id,username = Thisuser.username,  firstname = Thisuser.firstname,  
                middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                dateTimeCreated = ThisStaff.dateTimeCreated, designation=  ThisStaff.designation, 
                department= ThisStaff.department, is_Active= ThisStaff.is_Active) 
def get_staff_ver2(username: str, db: Session ) -> Staff:    
    queryResult = db.query(Users, Staffs).join(Staffs, Users.id == Staffs.user_id)
    ThisUserAndStaff = queryResult.filter(func.trim(func.lower(Users.username)) == username.strip().lower()).first()
    if ThisUserAndStaff is None :
         return ThisUserAndStaff   
    Thisuser, ThisStaff=  ThisUserAndStaff  # unpacks     
    return Staff(id = ThisStaff.id,username = Thisuser.username,  firstname = Thisuser.firstname,  
                middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                dateTimeCreated = ThisStaff.dateTimeCreated, designation=  ThisStaff.designation, 
                department= ThisStaff.department, is_Active= ThisStaff.is_Active) 
def get_staff_by_email_ver2(emailAddy: str, db: Session ) -> Staff:  
    queryResult = db.query(Users, Staffs).join(Staffs, Users.id == Staffs.user_id)
    ThisUserAndStaff = queryResult.filter(func.trim(func.lower(Users.emailAddy)) == emailAddy.strip().lower()).first()
    if ThisUserAndStaff is None :
        return ThisUserAndStaff
    Thisuser, ThisStaff=  ThisUserAndStaff  # unpacks      
    return Staff(id = ThisStaff.id,username = Thisuser.username,  firstname = Thisuser.firstname,  
                middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                dateTimeCreated = ThisStaff.dateTimeCreated, designation=  ThisStaff.designation, 
                department= ThisStaff.department, is_Active= ThisStaff.is_Active)
def get_staffs_all(skip:int, limit:int, db: Session ) -> Staff: 
    staffs = db.query(Staffs).offset(skip).limit(limit).all()
    if staffs is None:
        raise HTTPException(status_code=404, detail=f"Staffs(skip={skip}, limit={limit}) not found")  
    lstStaffs: list[Staff]= []
    for staff in staffs:    
        ThisStaff =  Staff(id = staff.id, username = staff.user.username, firstname = staff.user.firstname,  
                middlename = staff.user.middlename, lastname = staff.user.lastname,emailAddy = staff.user.emailAddy, 
                dateTimeCreated = staff.dateTimeCreated,  designation= staff.designation, department=staff.department, 
                is_Active= staff.is_Active)       
        lstStaffs.append(ThisStaff)
    if not lstStaffs: # if list is empty
        raise HTTPException(status_code=404, detail=f"Staffs(skip={skip}, limit={limit}) not found")  
    return lstStaffs