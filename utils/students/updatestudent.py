from fastapi import   HTTPException
from sqlalchemy.orm import Session 
from sqlalchemy import func
from schemas.students.studentupdate import StudentUpdate
from schemas.users.user import User 
from schemas.students.student import Student
def update_student(student: StudentUpdate, db: Session ) -> Student:  
   try: 
    from models.accounts import  Users, Students
    queryResult = db.query(Users, Students).join(Students, Users.id == Students.user_id)
    ThisUserAndStudent = queryResult.filter(func.trim(func.lower(Users.emailAddy)) == student.emailAddy.strip().lower()).first()    
    if ThisUserAndStudent is None:
       raise HTTPException(status_code=404, detail=f"Student(email={student.emailAddy}) does not exist in DB.")
    Thisuser, ThisStudent =  ThisUserAndStudent  # unpacks 
    if Thisuser.username != student.username:
        raise HTTPException(status_code=404, detail=f"Student(username={student.username}) does not match in DB.")
    db.reset() # resets the database session
    db.begin()
    Thisuser.firstname = student.firstname  
    Thisuser.middlename = student.middlename 
    Thisuser.lastname = student.lastname 
    ThisStudent.programme = student.program
    ThisStudent.level = student.level
    db.add(Thisuser) 
    db.add(ThisStudent)
    db.commit()    
    return Student(id = ThisStudent.id,username = student.username,  firstname = student.firstname,  
                middlename = student.middlename, lastname = student.lastname,emailAddy = student.emailAddy, 
                dateTimeCreated = ThisStudent.dateTimeCreated, programme= ThisStudent.programme, level= ThisStudent.level,
                is_Active= ThisStudent.is_Active)    
   except Exception as e:
        db.rollback()
        raise e