from fastapi import HTTPException 
from sqlalchemy.orm import Session 
from sqlalchemy import func
from models.accounts import Users, Students 
from schemas.general.login import  Login
from schemas.students.student import Student, StudentAUTH
import hashlib

import httpx
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional  

# Pydantic model (as defined above)
class StudentProfile(BaseModel):
    surname: str
    firstname: str
    othernames: str
    sex: str
    program: str
    program_code: str
    dpt: str
    college: str
    college_id: str
    level: int
    email: str
    email_alternate: str
    isFresher: str
    accom_paid: float
    accom_payable: float
    special_accom_paid: Optional[float]  # -1 indicates no special accommodation
    special_accom_payable: float
    accountBalance: float
    exemption_id: Optional[int]
    exemption_reason: str

def LoginStudent(payload: Login, db: Session ):  
   try:     
       ThisUser = None   
       placeHolderLabel = "username" 
       placeHolderValue = ""
       if payload.username.strip().lower() !=  "":  # login with username, ie matric number
        ThisUser = db.query(Users).filter(func.lower(func.trim(Users.username)) == payload.username.strip().lower()).first()  
        placeHolderValue = payload.username  
       if ThisUser is None: 
            try:
                oStudentProfile: StudentProfile =  getStudentProfileFromPortal(payload) 
                from sqlalchemy.orm import Session 
                from utils.students.createstudent import  create_student
                from schemas.students.studentcreate import StudentCreate              
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
                return create_student(oStudentCreate, db)           
            except  Exception as e:
                raise e               
            
       '''   # password is not needed
       password = hashlib.md5(payload.password.strip().encode()).hexdigest()            
       if ThisUser.password != password:
           raise HTTPException(status_code=404, detail=f"User({placeHolderLabel}={placeHolderValue})'s password does not match DB's.")
       '''
       queryResult = db.query(Users, Students).join(Students, Users.id == Students.user_id)
       ThisUserAndStudent= queryResult.filter(Users.id == ThisUser.id).first() 
       if ThisUserAndStudent is None:
           raise HTTPException(status_code=404, detail=f"Student(username={payload.username}) does not exist in DB.")      
           
       '''
       if ThisUser.isVerifiedEmail is False:          
            if ThisUserAndStudent is None:
                raise HTTPException(status_code=404, detail=f"Admin({placeHolderLabel}={placeHolderValue}) does not exist in DB.")      
            from models.accounts import vTokens
            Token = db.query(vTokens).filter(vTokens.user_id == ThisUser.id).first()
            if  Token is None:                    
                    import random
                    ten_digit =  str(int(''.join(str(random.randint(0,9)) for _ in range(10)))) # email verification token
                    db_vToken = vTokens(emailVerificationToken = ten_digit, user_id = ThisUser.id) # inserts verification token 
                    db.add(db_vToken) 
                    db.commit()
            else: # unused token exists for ThisUser...resuse                
                ten_digit =  Token.emailVerificationToken
            sendVerificationCodeToAdmin(ten_digit, payload)   
            raise HTTPException(status_code=404, detail=f"Student({placeHolderLabel}={placeHolderValue}) account is awaiting verification...check your inbox.") 
       '''
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
       #return {"access_token": access_token, "token_type": "bearer"}
       student= Student(id = ThisStudent.id,  username = ThisUser.username,  firstname = ThisUser.firstname,  
                        middlename = ThisUser.middlename, lastname = ThisUser.lastname,
                        emailAddy = ThisUser.emailAddy, programme = ThisStudent.programme, 
                        level = ThisStudent.level, is_UG = True,
                        dateTimeCreated = ThisStudent.dateTimeCreated, is_Active= ThisStudent.is_Active) 

       return StudentAUTH(student = student,
                        token = access_token)
   except Exception as e: 
        db.rollback()        
        raise e
def getStudentProfileFromPortal(payload:Login) -> StudentProfile:
    #raise HTTPException(status_code=404, detail=f"User('matric number' = {payload.username}') does not exist in DB.") 
    try:
        return  get_student_profile(payload.username)  
    except Exception as e:
        raise e
    # raise HTTPException(status_code=404, detail=f"User('matric number' = {payload.username} - {student_profile.firstname}') does not exist in DB.") 

def sendVerificationCodeToAdmin(ten_digit:str,payload:Login):        
      from infrastructure.emailer  import  sendEmail   
      code = f"{ten_digit}{payload.emailAddy.strip().lower()}"
      code = hashlib.md5(code.encode()).hexdigest()
      retMsg =  sendEmail(processor =  payload.processor, subject="Verify Student",
                          message="Please use the link below to verify your email account", 
                          receiver_email= payload.emailAddy, code = code, uri = payload.frontendURL)    



def get_student_profile(matric_number: str) -> StudentProfile:
    try:

        url = f"https://reg.run.edu.ng/apis/profile/getstudent?matric={matric_number}"  # Replace with actual API URL
        # Using httpx to make the synchronous GET request to the remote API
        with httpx.Client() as client:
            response = client.get(url) 
        # If the response is not successful, raise an error
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch student profile")     
        # Parse and return the JSON data using Pydantic model validation
        return StudentProfile.parse_obj(response.json())
    except Exception as e:
        raise e