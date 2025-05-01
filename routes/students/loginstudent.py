from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session
from utils.students.loginstudent import LoginStudent
from models.database import  get_db
from schemas.students.student import Student, StudentAUTH
from schemas.general.login import Login 
router = APIRouter()     
@router.post("/loginStudent/", include_in_schema=True, response_model = StudentAUTH)          
async def do(payload: Login = Body(..., embed= True), db: Session = Depends(get_db)):
   return LoginStudent(payload, db)
