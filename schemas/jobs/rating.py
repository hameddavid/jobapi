from pydantic import BaseModel, ConfigDict, Field, conint, constr
from typing import Optional
from datetime import datetime
from models.jobs import RateType
from schemas.jobs.job import SimpleJobSchema 
from schemas.users.user import User as UserSchema






class RatingCreateSchema(BaseModel):
    job_id: int = Field(..., description="ID of the job for which the owner is being rated.")
    job_owner_id: int = Field(..., description="ID of the job owner being rated.") 
    job_doer_id: int = Field(..., description="ID of the job doer who is rating the owner.")
    rating: conint(ge=1, le=5) = Field(..., description="Rating from 1 to 5 stars.")
    review_text: Optional[constr(max_length=1000)] = Field(None, description="Optional review text.")
   

    model_config = ConfigDict(from_attributes=False)


class RatingResponseSchema(BaseModel):
    id: int
    # job_id: int
    job_doer_id: int
    job_owner_id: int
    rating: int
    rate_type: RateType
    review_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
    

class ListRatingSchema(BaseModel):
    id: int
    job: Optional[SimpleJobSchema] = None # Assuming ListJobSchema is for a single Job
    job_doer: Optional[UserSchema] = None
    job_owner: Optional[UserSchema] = None
    rating: int
    rate_type: RateType
    review_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
    
class ListDoerRatingSchema(BaseModel):
    id: int
    job: Optional[SimpleJobSchema] = None # Assuming ListJobSchema is for a single Job
    job_doer: Optional[UserSchema] = None
    job_owner: Optional[UserSchema] = None
    rating: int
    rate_type: RateType
    review_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ListOwnerRatingSchema(BaseModel):
    id: int
    job: Optional[SimpleJobSchema] = None # Assuming ListJobSchema is for a single Job
    job_doer: Optional[UserSchema] = None
    job_owner: Optional[UserSchema] = None
    rating: int
    rate_type: RateType
    review_text: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)