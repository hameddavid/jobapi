from fastapi import HTTPException 
from sqlalchemy.orm import Session 
from sqlalchemy import func
from models.accounts import Users, Students 
from schemas.general.login import  Login
from schemas.students.student import Student, StudentAUTH 
from fastapi import HTTPException  
from utils.general.getRunStudentProfile import StudentProfile
def LoginStudent(payload: Login, db: Session ) -> StudentAUTH:  
   try:     
       ThisUser = None   
       placeHolderLabel = "username" 
       placeHolderValue = ""
       if payload.username.strip().lower() ==  "":  # login with username, ie matric number
           raise HTTPException(status_code=404, detail=f"Student(username cannot be empty!")      
       ThisUser = db.query(Users).filter(func.lower(func.trim(Users.username)) == payload.username.strip().lower()).first()  
       placeHolderValue = payload.username  
       if ThisUser is None: 
            try:
                oStudentProfile: StudentProfile =  getStudentProfileFromPortal(payload)                
                from utils.students.createstudent import  create_student
                from schemas.students.studentcreate import StudentCreate   
                from infrastructure.emailer import is_valid_email               
                if is_valid_email(oStudentProfile.email) == False:
                     raise HTTPException(status_code=404, detail=f"Student(email={oStudentProfile.email}) is not valid")          
                oStudentCreate = StudentCreate(   
                    username =  payload.username,                    
                    emailAddy = oStudentProfile.email,
                    firstname = oStudentProfile.firstname,
                    middlename = oStudentProfile.othernames,
                    lastname = oStudentProfile.surname,
                    password = f"{payload.password}", 
                    programme = oStudentProfile.program_code, 
                    level = oStudentProfile.level,
                    is_UG = True
                    )
                create_student(oStudentCreate, db)   
                ThisUser = db.query(Users).filter(func.lower(func.trim(Users.username)) == payload.username.strip().lower()).first()          
                if ThisUser is None:
                    raise HTTPException(status_code=404, detail=f"User(username= {payload.username}) is not valid!")
            except  Exception as e:
                raise HTTPException(status_code=404, detail=f"{e}")          
       queryResult = db.query(Users, Students).join(Students, Users.id == Students.user_id)
       ThisUserAndStudent= queryResult.filter(Users.id == ThisUser.id).first() 
       if ThisUserAndStudent is None:
           try:
            ThisUserAndStudent = insert_student(ThisUser, payload, db)
            if ThisUserAndStudent is None:
                raise HTTPException(status_code=404, detail=f"Student ({payload.username}, {payload.emailAddy} ) not created!")
           except Exception as e:
            raise HTTPException(status_code=404, detail=f"{e}")      
       _ , ThisStudent =   ThisUserAndStudent
       if ThisStudent.is_Active == False:
           raise HTTPException(status_code=404, detail=f"Student({placeHolderLabel}={placeHolderValue}) account requires activation by ADMIN.") 
       from utils.general.authentication import   ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
       from utils.general.authentication import Token, timedelta 
       ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Set token expiration to 1 hour
       access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
       access_token = create_access_token(
        data={"sub": ThisUser.username}, expires_delta=access_token_expires
          )         
       student= Student(id = ThisStudent.id,  username = ThisUser.username,  firstname = ThisUser.firstname,  
                        middlename = ThisUser.middlename, lastname = f"{ThisUser.lastname}",
                        emailAddy = ThisUser.emailAddy, programme = ThisStudent.programme, 
                        level = ThisStudent.level, is_UG = True,
                        dateCreated = ThisStudent.dateTimeCreated, is_Active= ThisStudent.is_Active) 
       return StudentAUTH(student = student,
                        token = access_token)
   except Exception as e: 
        db.rollback()    
        raise HTTPException(status_code=404, detail=f"{str(e)}")    
        
def  insert_student(ThisUser, payload: Login,db:Session):
    try:
        oStudentProfile: StudentProfile =  getStudentProfileFromPortal(payload) 
        db_student = Students(programme = oStudentProfile.program_code, level = oStudentProfile.level,
                            user_id =  ThisUser.id)
        db.add(db_student)         
        db.commit()  
        db.refresh(db_student) 
        queryResult =  db.query(Users, Students).join(Students, Users.id == Students.user_id) 
        return queryResult.filter(Users.id == ThisUser.id).first()
    except Exception as e:
        raise e

def getStudentProfileFromPortal(payload:Login) -> StudentProfile:    
    try:
        from utils.general.getRunStudentProfile import get_student_profile
        return  get_student_profile(payload.username)  
    except Exception as e:
        raise e
 