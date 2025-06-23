from pydantic import BaseModel, ConfigDict,Field
from fastapi import UploadFile, File, Form
from datetime import datetime
from models.applications import AppStatus
from schemas.users.user import User
from typing import Optional,List
from schemas.jobs.job import ListJobSchema


class CreateAppSchema(BaseModel): 
    title: str
    narration: Optional[str] = Form(None, description="Your cover letter text"),  
    doc_1: UploadFile = File(..., description="Your resume document (PDF, DOCX, jpeg.)"),
    suitable_price: float
    job_id:  int = Form(..., description="ID of the job to apply for")
  


    model_config = ConfigDict(from_attributes=True)
    
    
    
#    job_id: int = Form(..., description="ID of the job to apply for"),
#     cover_letter: Optional[str] = Form(None, description="Your cover letter text"),
    
#     resume: UploadFile = File(..., description="Your resume document (PDF, DOCX, jpeg.)"),
#     other_documents: Optional[List[UploadFile]] = File(None, description="Optional additional supporting documents"),
    
class UpdateAppSchema(BaseModel): 
    id: int
    title: str
    narration: str  
    doc_1: str
    doc_2: str
    doc_3: str
    image: str
    suitable_price: float



    model_config = ConfigDict(from_attributes=True)   
    
class CreateAppRespSchema(BaseModel):
    id: int  
    title: str
    narration: str  
    doc_1: str
    suitable_price: float
    status:AppStatus
    rejection_reason: Optional[str] = None
    dateTimeCreated: datetime
    dateTimeUpdated: datetime
    job_id:  int
    user_id:  int
    deleted: str = 'N'

    class Config:
        orm_mode = True  
    # model_config = ConfigDict(from_attributes=True)
    
    

class GetAppSchema(BaseModel):
    id: int  
    title: str
    narration: str  
    doc_1: str
    doc_2: str
    doc_3: str
    image: str
    suitable_price: float
    status:AppStatus
    rejection_reason: Optional[str] = None
    dateTimeCreated: datetime
    dateTimeUpdated: datetime
    job:  ListJobSchema
    owner:  User
    # deleted: str = 'N'

    
    model_config = ConfigDict(from_attributes=True)