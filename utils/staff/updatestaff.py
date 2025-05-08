from fastapi import HTTPException
from sqlalchemy.orm import Session 
from sqlalchemy import func
from schemas.staff.staffupdate import StaffUpdate 
from schemas.staff.staff import Staff
def update_staff(staffUser: StaffUpdate, db: Session ) -> Staff:  
   try:       
    from models.accounts import  Users, Staff as Staffs
    queryResult = db.query(Users, Staffs).join(Staffs, Users.id == Staffs.user_id)
    ThisUserAndStaff = queryResult.filter(func.trim(func.lower(Users.emailAddy)) == staffUser.emailAddy.strip().lower()).first()    
    if ThisUserAndStaff is None:
       raise HTTPException(status_code=404, detail=f"Staff(email={staffUser.emailAddy}) does not exist in DB.")
    Thisuser, ThisStaff =  ThisUserAndStaff  # unpacks 
    if Thisuser.username != staffUser.username:
        raise HTTPException(status_code=404, detail=f"Staff(username={staffUser.username}) does not match in DB.")
    db.reset() # resets the database session
    db.begin()
    Thisuser.firstname = staffUser.firstname  
    Thisuser.middlename = staffUser.middlename 
    Thisuser.lastname = staffUser.lastname 
    ThisStaff.designation = staffUser.designation
    ThisStaff.department = staffUser.department
    db.add(Thisuser) 
    db.add(ThisStaff)
    db.commit()   
    return Staff(id = ThisStaff.id, username = Thisuser.username,  firstname = staffUser.firstname,  
                    middlename = staffUser.middlename, lastname = staffUser.lastname,emailAddy = staffUser.emailAddy, 
                    dateTimeCreated = ThisStaff.dateTimeCreated, designation= ThisStaff.designation, 
                    department = ThisStaff.department, is_Active=  ThisStaff.is_Active)     
   except Exception as e:
        db.rollback()
        raise e   
  