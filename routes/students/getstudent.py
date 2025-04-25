from fastapi import APIRouter, Depends 
from sqlalchemy.orm import Session 
from utils.students.getstudent import get_student, get_student_by_email, get_students_all
from models.database import  get_db 
from schemas.students.student import Student
from schemas.users.user import User
from utils.general.authentication import get_current_user
from urllib.parse import unquote
router = APIRouter()
@router.get("/getstudent",
            include_in_schema=True,response_model= Student)
async def do(username: str, db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):      
    return get_student(username, db)
@router.get("/getstudentbyemail",
            include_in_schema=True, 
            response_model= Student)
async def do(email: str, db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):   
    return get_student_by_email(email, db) 
@router.get("/getstudents",
            include_in_schema=True, 
            response_model= list[Student])
async def do(skip: int = 0, limit:int = 100,
                    db: Session = Depends(get_db),TheUser: User = Depends(get_current_user) ):   
    return get_students_all(skip, limit, db)
