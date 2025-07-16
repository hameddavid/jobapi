# routers/ratings.py

from fastapi import  Depends, status
from typing import List
from sqlalchemy.orm import Session
from models.database import get_db
from models.accounts import Users
from .router import router    
from schemas.jobs.rating import ListRatingSchema
from utils.general.authentication import get_current_user
from utils.rating.getRating import get_rating_by_id,list_all_rating,list_owner_rating,list_doer_rating,get_rating_giving_user_id



@router.get("/get_rating", response_model=ListRatingSchema, status_code=status.HTTP_200_OK)
def get_rating(
    rate_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user) ):
    
    return get_rating_by_id(
        rate_id,
        db,
        current_user
    )
    
   


@router.get("/get_rating_giving_user_id", response_model='', status_code=status.HTTP_200_OK)
def get_user_rating(
    user_id: int,
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user) ):
    
    return get_rating_giving_user_id(
        user_id,
        skip, 
        limit,
        db,
        current_user
    )
    

@router.get("/list_all_rating", response_model=List[ListRatingSchema], status_code=status.HTTP_200_OK)
def list_rating(
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user) ):
    
    return list_all_rating(
        skip,
        limit,
        db,
        current_user
    )

@router.get("/list_owner_rating", response_model=List[ListRatingSchema], status_code=status.HTTP_200_OK)
def list_owner(
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user) ):
    
    return list_owner_rating(
        skip,
        limit,
        db,
        current_user
    )
    

@router.get("/list_doer_rating", response_model=List[ListRatingSchema], status_code=status.HTTP_200_OK)
def list_doer(
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user) ):
    
    return list_doer_rating(
        skip,
        limit,
        db,
        current_user
    )