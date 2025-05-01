from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session  
from models.database import  get_db 
from schemas.students.student import Student
from schemas.students.studentupdate import  StudentUpdate 
from utils.students.updatestudent import update_student
from schemas.users.user import User
from utils.general.authentication import get_current_user
router = APIRouter()     
@router.put("/updateStudent/", response_model=Student)         # update user if it exists
async def do(user: StudentUpdate = Body(..., embed= True), db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):
   return update_student(user, db)
