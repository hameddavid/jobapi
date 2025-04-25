from fastapi import   HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.accounts import  Users, Students
from schemas.students.student import Student 
def get_student(username: str, db: Session ) -> Student:        
    queryResult = db.query(Users, Students).join(Students, Users.id == Students.user_id)
    ThisUserAndStudent = queryResult.filter(func.trim(func.lower(Users.username)) == username.strip().lower()).first()
    if ThisUserAndStudent is None :
        raise HTTPException(status_code=404, detail = f"Student(username={username}) not found")    
    Thisuser, ThisStudent =  ThisUserAndStudent  # unpacks
    return Student(id = ThisStudent.id,username = Thisuser.username,  firstname = Thisuser.firstname,  
                middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                dateCreated = ThisStudent.dateTimeCreated, programme= ThisStudent.programme, level= ThisStudent.level,
                is_Active= ThisStudent.is_Active,is_UG = ThisStudent.is_UG)       
def get_student_by_email(emailAddy: str, db: Session ) -> Student:    
    queryResult = db.query(Users, Students).join(Students, Users.id == Students.user_id)
    ThisUserAndStudent = queryResult.filter(func.trim(func.lower(Users.emailAddy)) == emailAddy.strip().lower()).first()
    if ThisUserAndStudent is None :
        raise HTTPException(status_code=404, detail = f"Student(emailAddy = {emailAddy}) not found")    
    Thisuser, ThisStudent = ThisUserAndStudent   # unpacks
    return Student(id = ThisStudent.id,username = Thisuser.username,  firstname = Thisuser.firstname,  
                middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                dateCreated = ThisStudent.dateTimeCreated, programme= ThisStudent.programme, level= ThisStudent.level,
                is_Active= ThisStudent.is_Active,is_UG = ThisStudent.is_UG) 
def get_student_ver2(username: str, db: Session ) -> Student:    
    queryResult = db.query(Users, Students).join(Students, Users.id == Students.user_id)
    ThisUserAndStudent = queryResult.filter(func.trim(func.lower(Users.username)) == username.strip().lower()).first()
    if ThisUserAndStudent is None :
       return   ThisUserAndStudent
    Thisuser, ThisStudent =  ThisUserAndStudent  # unpacks
    return Student(id = ThisStudent.id,username = Thisuser.username,  firstname = Thisuser.firstname,  
                middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                dateCreated = ThisStudent.dateTimeCreated, programme= ThisStudent.programme, level= ThisStudent.level,
                is_Active= ThisStudent.is_Active,is_UG = ThisStudent.is_UG)  
def get_student_by_email_ver2(emailAddy: str, db: Session ) -> Student:  
    queryResult = db.query(Users, Students).join(Students, Users.id == Students.user_id)
    ThisUserAndStudent = queryResult.filter(func.trim(func.lower(Users.emailAddy)) == emailAddy.strip().lower()).first()
    if ThisUserAndStudent is None :
        return ThisUserAndStudent
    Thisuser, ThisStudent = ThisUserAndStudent   # unpacks
    return Student(id = ThisStudent.id,username = Thisuser.username,  firstname = Thisuser.firstname,  
                middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                dateCreated = ThisStudent.dateTimeCreated, programme= ThisStudent.programme, level= ThisStudent.level,
                is_Active= ThisStudent.is_Active,is_UG = ThisStudent.is_UG)
def get_students_all(skip:int, limit:int, db: Session ) -> list[Student]:  
    students = db.query(Students).offset(skip).limit(limit).all()
    if students is None:
        raise HTTPException(status_code=404, detail=f"Students(skip={skip}, limit={limit}) not found")  
    lstStudents: list[Student]= []
    for student in students:    
        ThisStudent = Student(id = student.id,username = student.user.username,  firstname = student.user.firstname,  
                middlename = student.user.middlename, lastname = student.user.lastname,emailAddy = student.user.emailAddy, 
                dateCreated = student.dateTimeCreated, programme= student.programme, level= student.level,
                is_Active= student.is_Active, is_UG = student.is_UG)        
        lstStudents.append(ThisStudent)
    if not lstStudents: # if list is empty
        raise HTTPException(status_code=404, detail=f"Students(skip={skip}, limit={limit}) not found")  
    return lstStudents 