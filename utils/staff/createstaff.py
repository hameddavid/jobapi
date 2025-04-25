from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.accounts import  Users, Staff as Staffs
from schemas.users.usercreate import UserCreate
from schemas.users.user import User
from schemas.staff.staffcreate import StaffCreate
from schemas.staff.staff import Staff 
from ..users.createuser import  create_user_ver2
def create_staff(staffUser: StaffCreate, db: Session ) -> Staff:  
    try:              
        userCreate:UserCreate = UserCreate(username = staffUser.username, password = staffUser.password, 
                        firstname = staffUser.firstname, 
                        middlename = staffUser.middlename,
                        lastname = staffUser.lastname,
                        emailAddy = staffUser.emailAddy,
                        processor= "",   # not applicable
                        frontendurl = "" # not applicable
                        )
        db.reset()
        db.begin()
        import hashlib, random
        ten_digit =  str(int(''.join(str(random.randint(0,9)) for _ in range(10)))) # email verification token
        #password = hashlib.md5(staffUser.password.encode()).hexdigest()  # not using this result 
        user:User = create_user_ver2(userCreate, staffUser.password, ten_digit, db)   # if exception is raised...rollback will happen        
        queryResult = db.query(Users, Staffs).join(Staffs, Users.id == Staffs.user_id)
        ThisUserAndStaff = queryResult.filter(Users.username == staffUser.username).first()
        if ThisUserAndStaff:
            raise HTTPException(status_code=404, detail=f"Staff(emailAddy={staffUser.emailAddy}) exists in DB.")
        db_staff = Staffs(designation= staffUser.designation, department= staffUser.department, user_id =  user.id) # inserts new operator in DB
        db.add(db_staff)         
        db.commit()  
        db.refresh(db_staff)
        return Staff(id = db_staff.id,  username = staffUser.username,  firstname = staffUser.firstname,  
                        middlename = staffUser.middlename, lastname = staffUser.lastname,emailAddy = staffUser.emailAddy, 
                        dateCreated = db_staff.dateTimeCreated, designation= db_staff.designation, department= db_staff.department,
                        is_Active= db_staff.is_Active)
    except Exception as e:
            db.rollback()  # rolls back transaction if there is any failure
            raise e   