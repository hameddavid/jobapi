from pydantic import BaseModel,ConfigDict,Field
from datetime import datetime
from schemas.users.user import User as UserSchema
from schemas.apps.appschema import GetAppSchema



class CreateJobAllocation(BaseModel):
    app_id: int

    
    
    # model_config = ConfigDict(from_attributes=True)
    
    
    
class JobAllocation(BaseModel):
    id: int
    application: GetAppSchema
    dateTimeJobStarted: datetime
    dateTimeJobCompleted: datetime
    dateTimeJobClosed: datetime
    dateTimePaymentMade: datetime
    dateTimePaymentConfirmed: datetime
    paymentReceiptURL: str
    dateTimeCreated: datetime
    dateTimeUpdated: datetime
    deleted: str = 'N'    


