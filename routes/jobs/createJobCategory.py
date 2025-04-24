from fastapi import APIRouter, Depends, Body 
from sqlalchemy.orm import Session
from utils.admins.createadmin import   create_admin
from models.database import  get_db
from schemas.admins.admin import Admin
from schemas.admins.admincreate import AdminCreate 
router = APIRouter()     
@router.post("/createJobCategory/", include_in_schema=True, response_model=Admin)          
async def do(user: AdminCreate = Body(..., embed= True), db: Session = Depends(get_db)):
   return create_admin(user, db)