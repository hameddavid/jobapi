# routers/ratings.py

from fastapi import  Depends, status
from sqlalchemy.orm import Session
from models.database import get_db
from models.accounts import Users # For current_user
from utils.rating.createRating import create_rating_for_job_owner,create_rating_for_job_doer
from .router import router   
from schemas.jobs.rating import RatingCreateSchema, RatingResponseSchema
from utils.general.authentication import user_required_roles



@router.post("/job-owner/", response_model=RatingResponseSchema, status_code=status.HTTP_201_CREATED)
def job_owner(
    rating_data: RatingCreateSchema = Depends(),
    db: Session = Depends(get_db),
    current_user: Users = Depends(user_required_roles(["student","staff"])) # The job doer
):
    return create_rating_for_job_owner(
        rating_data=rating_data,
        db=db,
        current_user=current_user
    )
    
    

@router.post("/job-doer/", response_model=RatingResponseSchema, status_code=status.HTTP_201_CREATED)
def job_doer(
    rating_data: RatingCreateSchema = Depends(),
    db: Session = Depends(get_db),
    current_user: Users = Depends(user_required_roles(["student","staff"])) # The job doer
):
    return create_rating_for_job_doer(
        rating_data=rating_data,
        db=db,
        current_user=current_user
    )