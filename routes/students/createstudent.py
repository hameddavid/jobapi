from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session 
from utils.students.createstudent import  create_student
from models.database import  get_db
from schemas.students.student import Student
from schemas.students.studentcreate import StudentCreate 
router = APIRouter()     
@router.post("/createStudent/", include_in_schema=True, response_model=Student)          
async def do(student: StudentCreate = Body(..., embed= True), db: Session = Depends(get_db)):
   return create_student(student, db)
