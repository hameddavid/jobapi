from pydantic import BaseModel, ConfigDict,Field
from datetime import datetime
from models.applications import AppStatus



class CreateAppSchema(BaseModel):
    id: int  
    title: str
    narration: str  
    doc_1: str
    doc_2: str
    doc_3: str
    image: str
    suitable_price: float
    status:AppStatus
    user_id:  int    #   he posted the job
    app_category_id: int
    dateTimeCreated: datetime
    deleted: str = 'N'

    model_config = ConfigDict(from_attributes=True)
    
    
    
    
#   = Column(String(50), nullable=False) #  like title of application letter
#      = Column(String(500), nullable=False)  # like an application letter
#      = Column(String(200), nullable=True)  # path to doc on filesystem...may be empty
#      = Column(String(200), nullable=True)  # path to doc on filesystem...may be empty
#      = Column(String(200), nullable=True)  # path to doc on filesystem...may be empty
#      = Column(String(200), nullable=True)  # path to image on filesystem...may be empty
#      = Column(Integer, nullable=True)  #  amount expectations
#     status =  Column(SQLAlchemyEnum(AppStatus), default=AppStatus.SUBMITTED, nullable=False) 
#     rejection_reason = Column(String(500), nullable=True)  # reason for rejection
#     dateTimeCreated = Column(DateTime, default=datetime.utcnow)
#     dateTimeUpdated = Column(DateTime, default=datetime.utcnow)
#     job_id =  Column(Integer,  ForeignKey("jobs.id"), unique=True,nullable= False) # associated with a job  
#     user_id =  Column(Integer,  ForeignKey("users.id"), nullable= False)