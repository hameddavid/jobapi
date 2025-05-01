from fastapi import   HTTPException
from sqlalchemy.orm import Session
from schemas.users.usercreate import UserCreate
from schemas.users.user import User
from schemas.students.studentcreate import StudentCreate
from models.accounts import Students
from schemas.students.student import Student 
from ..users.createuser import create_user_ver2
def create_student(student: StudentCreate, db: Session ) -> Student:  
    try:       
        userCreate:UserCreate = UserCreate(username = student.username, password = student.password, 
                        firstname = student.firstname, 
                        middlename = student.middlename,
                        lastname = student.lastname,
                        emailAddy = student.emailAddy,
                        processor=  "", # not applicable
                        frontendurl= ""  # not applicable
                        )
        db.reset()
        db.begin()
        import hashlib, random
        ten_digit =  str(int(''.join(str(random.randint(0,9)) for _ in range(10)))) # email verification token
        #password = hashlib.md5(student.password.encode()).hexdigest()  # not using this result 
        user:User = create_user_ver2(userCreate, student.password, ten_digit, db)   # if exception is raised...rollback will happen 
        from .getstudent import get_student_by_email_ver2
        if get_student_by_email_ver2(student.emailAddy, db):
             raise HTTPException(status_code=404, detail=f"Student(emailAddy={student.emailAddy}) exists in DB.")                    
        db_student = Students(programme = student.programme, level = student.level, user_id =  user.id)
        db.add(db_student)         
        db.commit()  
        db.refresh(db_student)        
        return Student(id = db_student.id,  username = student.username,  firstname = student.firstname,  
                    middlename = student.middlename, lastname = student.lastname,emailAddy = student.emailAddy, 
                    dateCreated = db_student.dateTimeCreated,  is_Active = db_student.is_Active,
                    programme = student.programme, level = student.level, is_UG = student.is_UG)     
    except Exception as e:
        db.rollback()  # rolls back transaction if there is any failure
        raise HTTPException(status_code=404, detail=f"create_student (error): {str(e)})") 

    