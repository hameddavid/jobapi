from fastapi import HTTPException 
from sqlalchemy.orm import Session 
from sqlalchemy import func
from models.accounts import Users, Staff as Staffs
from schemas.general.login import  LoginStaff
from schemas.staff.staff import Staff, StaffAUTH
from utils.general.authentication import assign_roles_and_create_token
from infrastructure.emailer import is_valid_email  
from utils.general.getRunStaffProfile  import StaffProfile  
def LoginStaff(payload: LoginStaff, db: Session ) -> StaffAUTH:  
   try:     
       ThisUser = None   
       placeHolderLabel = "emailAddy" 
       placeHolderValue = ""
       if not is_valid_email(payload.emailAddy):
        raise HTTPException(status_code=404, detail=f"Student(email={payload.emailAddy}) is not valid")  
       ThisUser = db.query(Users).filter(func.lower(func.trim(Users.emailAddy)) == payload.emailAddy.strip().lower()).first()  
       placeHolderValue = payload.emailAddy  
       if ThisUser is None: 
            try:
                oStaffProfile: StaffProfile =  getStaffProfileFromPortal(payload)                 
                from utils.staff.createstaff import  create_staff
                from schemas.staff.staffcreate import StaffCreate
                oStaffCreate = StaffCreate(   
                    username =  oStaffProfile.staff_no,                    
                    emailAddy = payload.emailAddy,
                    firstname = oStaffProfile.firstname,
                    middlename = oStaffProfile.middlename,
                    lastname = oStaffProfile.lastname,
                    password = f"{payload.password}", 
                    designation = oStaffProfile.staff_type, 
                    department = oStaffProfile.dept                    
                    )
                create_staff(oStaffCreate, db)  
                ThisUser = db.query(Users).filter(func.lower(func.trim(Users.emailAddy)) == payload.emailAddy.strip().lower()).first()           
                if ThisUser is None:
                    raise HTTPException(status_code=404, detail=f"Staff(emailAddy= {payload.emailAddy}) is not valid!")
            except  Exception as e:
                raise HTTPException(status_code=404, detail=f"{e}") 
       queryResult = db.query(Users, Staffs).join(Staffs, Users.id == Staffs.user_id)       
       ThisUserAndStaff= queryResult.filter(Users.id == ThisUser.id).first() 
       if ThisUserAndStaff is None:
           try:
            ThisUserAndStaff = insert_staff(ThisUser, payload, db)
            if ThisUserAndStaff is None:
                raise HTTPException(status_code=404, detail=f"Staff ({payload.username}, {payload.emailAddy} ) not created!")
           except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}") 
       _ , ThisStaff=   ThisUserAndStaff
       if not ThisStaff.is_Active:
           raise HTTPException(status_code=404, detail=f"Staff({placeHolderLabel}={placeHolderValue}) account requires activation by ADMIN.") 
       access_token = assign_roles_and_create_token(ThisUser, db) 
       roles = access_token.pop("roles", [])
       staff = Staff(id = ThisUser.id,  username = ThisUser.username,  firstname = ThisUser.firstname,  
                        middlename = ThisUser.middlename, lastname = f"{ThisUser.lastname}",
                        emailAddy = f"{ThisUser.emailAddy}", dateTimeCreated = ThisUser.dateTimeCreated, 
                        staff_id= ThisStaff.id,
                        designation= ThisStaff.designation, department= ThisStaff.department,
                        is_Active= ThisStaff.is_Active, roles= roles)    
       return StaffAUTH(staff = staff,
                        token = access_token)
   except Exception as e: 
        db.rollback()        
        raise HTTPException(status_code=404, detail=f"{e}")
def  insert_staff(ThisUser, payload:LoginStaff, db:Session):
    oStaffProfile: StaffProfile =  getStaffProfileFromPortal(payload)   
    db_staff = Staffs(designation= oStaffProfile.staff_type, department= oStaffProfile.dept, 
                      user_id =  ThisUser.id) # insert staff in DB
    db.add(db_staff)         
    db.commit()  
    db.refresh(db_staff) 
    queryResult =  db.query(Users, Staffs).join(Staffs, Users.id == Staffs.user_id) 
    return queryResult.filter(Users.id == ThisUser.id).first() 
def getStaffProfileFromPortal(payload:LoginStaff) -> StaffProfile:   
    try:
        from utils.general.getRunStaffProfile import get_staff_profile
        return  get_staff_profile(payload.emailAddy)  
    except Exception as e:
        raise e