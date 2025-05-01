from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.accounts import Admins
from schemas.users.usercreate import UserCreate
from schemas.users.user import User
from schemas.admins.admincreate import AdminCreate
from schemas.admins.admin import Admin 
from ..users.createuser import  create_user_ver2
import hashlib, random
def resendVerificationIfAdminIsNotYetVerified(admin:AdminCreate, db:Session):
    from models.accounts import Users,vTokens   
    ThisUser = db.query(Users).filter(func.trim(func.lower(Users.username)) == admin.username.strip().lower()).first()
    if ThisUser is None: # proceed to find user with email
        ThisUser = db.query(Users).filter(func.trim(func.lower(Users.emailAddy)) == admin.emailAddy.strip().lower()).first()
        if ThisUser is None:
            raise HTTPException(status_code=404, detail=f"User(Username = {admin.username} and EmailAddy={admin.emailAddy}) do not exist in DB.")
    ThisToken = db.query(vTokens).filter(vTokens.user_id == ThisUser.id).first()       
    if ThisToken is None:
        # token does not exist for the user...perhaps he is verified already       
        if ThisUser.isVerifiedEmail:
            return # he is verified
        else: # rare...recreate verification token            
            ten_digit =  str(int(''.join(str(random.randint(0,9)) for _ in range(10)))) # email verification token
            db_vToken = vTokens(emailVerificationToken = ten_digit, user_id = ThisUser.id) # inserts verification token 
            db.add(db_vToken) 
            db.commit()         
    else:  # Token exists...
        ten_digit:str = ThisToken.emailVerificationToken  # not yet verified...token exists... resend it
    sendVerificationCodeToAdmin(ten_digit,admin)     
def sendVerificationCodeToAdmin(ten_digit:str,admin:AdminCreate):        
      from infrastructure.emailer  import  sendEmail   
      code = f"{ten_digit}{admin.emailAddy.strip().lower()}"
      code = hashlib.md5(code.encode()).hexdigest()
      retMsg =  sendEmail(optTypeOfUser = "0", processor =  admin.processor, subject="Create Admin: JobPost",
                          message="Please use the link below to verify your email account", 
                          receiver_email= admin.emailAddy, code = code, uri = admin.frontendurl)


def create_admin(admin: AdminCreate, db: Session ):  
    try:   
        ## admin.password
        from utils.general.getRunStaffProfile import get_staff_profile, StaffProfile
        username:str = admin.username
        emailAddy:str= admin.emailAddy
        isStaff:bool = False
        isStudent:bool = False
        firstname:str =  ""
        middlename:str = ""
        lastname:str =   ""
        try:             
            oStaffProfile: StaffProfile = get_staff_profile(emailAddy) 
            username = oStaffProfile.userid # used staff id as username
            firstname = oStaffProfile.firstname
            middlename = oStaffProfile.middlename
            lastname = oStaffProfile.lastname
            isStaff = True   
        except Exception as e:  # not a staff
           
            from utils.general.getRunStudentProfile import get_student_profile,StudentProfile
            try:                
                oStudentProfile: StudentProfile  =  get_student_profile(username) 
                from infrastructure.emailer import is_valid_email               
                if is_valid_email(oStudentProfile.email) == False:
                     raise HTTPException(status_code=404, detail=f"Student(email={oStudentProfile.email}) is not valid")          
                firstname = oStudentProfile.firstname
                middlename = oStudentProfile.othernames
                lastname = oStudentProfile.surname 
                emailAddy = oStudentProfile.email # user email on students portal
                isStudent = True
            except Exception as e:  # neither a staff nor a student
                raise HTTPException(status_code=404, detail=f"Student validation failed: {e}")      
        if isStaff == False and isStudent == False :
            raise HTTPException(status_code=404, detail=f"Staff(emailAddy={emailAddy}) and Student(matric ={username}) not found in remote DBs.")
        userCreate:UserCreate = UserCreate(username = username, password = admin.password, 
                        firstname   =   firstname, 
                        middlename  =   middlename,
                        lastname    =   lastname,
                        emailAddy   =   emailAddy,
                        frontendurl =   admin.frontendurl,
                        processor   =   admin.processor)
        db.reset()
        db.begin()        
        ten_digit =  str(int(''.join(str(random.randint(0,9)) for _ in range(10)))) # email verification token
        password =  admin.password
        user:User = create_user_ver2(userCreate, password, ten_digit, db)   # if exception is raised...rollback will happen  
        from .getadmin import get_admin_by_email_ver2
        emailAddy = user.emailAddy  #  gets emailAddy from Users table
        ThisAdmin=   get_admin_by_email_ver2(emailAddy,db)  
        if ThisAdmin:  # already created an admin account for this User            
             resendVerificationIfAdminIsNotYetVerified(admin, db)
             raise HTTPException(status_code=404, detail=f"Admin(emailAddy={emailAddy}) exists in DB.")      
        try:             
            db_admin= Admins(user_id =  user.id) # inserts new admin in DB
            db.add(db_admin)         
            db.commit()  
            db.refresh(db_admin)
            ret =  Admin(id = db_admin.id,  username = username,  firstname = firstname,  
                        middlename = middlename, lastname = lastname,emailAddy = emailAddy, 
                        dateCreated = db_admin.dateTimeCreated,    is_Active= db_admin.is_Active)
        except Exception as e:
            db.rollback()  # rolls back transaction if there is any failure
            raise HTTPException(status_code=404, detail = f"{e}")    
        sendVerificationCodeToAdmin(ten_digit, admin)
        return ret        
    except Exception as e:
        db.rollback()  # rolls back transaction if there is any failure
        raise  e   