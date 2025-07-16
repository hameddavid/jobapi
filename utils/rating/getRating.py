from fastapi import   HTTPException
from sqlalchemy.orm import Session,joinedload
from models.accounts import Users 
from models.jobs import Rating as RatingModel
from schemas.users.user import User as UserSchema
from sqlalchemy import  or_
from schemas.jobs.job import SimpleJobSchema
from schemas.jobs.rating import ListRatingSchema,ListDoerRatingSchema,ListOwnerRatingSchema
from typing import List






def get_rating_by_id(
    rate_id: int,
    db: Session,
    current_user: Users
):
    try:
        
        query = (
                db.query(RatingModel)
                .options(
                    joinedload(RatingModel.job),
                    joinedload(RatingModel.owner),
                    joinedload(RatingModel.doer),
                )
                .filter(RatingModel.id == rate_id)
                .first()
            )
        
        if not query:
            raise HTTPException(
                status_code=404,
                detail="Rating not found"
            )

        job = SimpleJobSchema.model_validate({
            "id": query.job.id,
            "title": query.job.title,
            "description": query.job.description,
            "location": query.job.location,
            "listed_price": query.job.listed_price,
            "status": query.job.status,
            "dateTimeCreated": query.job.dateTimeCreated,
            "deleted": query.job.deleted,
            }) if query.job else None
        owner = UserSchema.model_validate(query.owner) if query.owner else None
        doer = UserSchema.model_validate(query.doer) if query.doer else None
    
    
        return ListRatingSchema.model_validate( {
            "id":query.id,
            "job": job,
            "job_doer":doer,
            "job_owner":owner,
            "rating":query.rating,
            "rate_type":query.rate_type,
            "review_text":query.review_text,
            "created_at":query.created_at,
            "updated_at":query.updated_at
    })
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Getting rating: {str(e)}"
        )



def get_rating_giving_user_id(
    user_id: int,
    skip: int, 
    limit: int,
    db: Session,
    current_user: Users
):
    try:
        
        queries = (
                db.query(RatingModel)
                .options(
                    joinedload(RatingModel.job),
                    joinedload(RatingModel.owner),
                    joinedload(RatingModel.doer),
                )
                .filter(
                    or_(
                     RatingModel.job_doer_id == user_id,
                     RatingModel.job_owner_id == user_id  
                    )) 
                .offset(skip)
                .limit(limit)
            )
        
        if not queries:
            raise HTTPException(
                status_code=404,
                detail=f"Rating not found for user with ID {user_id}"
            )

        list_owner_ratings: List[ListRatingSchema] = []
        list_doer_ratings: List[ListRatingSchema] = []
        count_doer = 0
        count_owner = 0
        aggre_doer = 0
        aggre_owner = 0
        for query in queries:
            if not query:
                continue
            if query.rate_type.value == "OWNER":
               count_owner += 1
               aggre_owner += query.rating
               job = SimpleJobSchema.model_validate({
                    "id": query.job.id,
                    "title": query.job.title,
                    "description": query.job.description,
                    "location": query.job.location,
                    "listed_price": query.job.listed_price,
                    "status": query.job.status,
                    "dateTimeCreated": query.job.dateTimeCreated,
                    "deleted": query.job.deleted,
                    }) if query.job else None
               owner = UserSchema.model_validate(query.owner) if query.owner else None
               doer = UserSchema.model_validate(query.doer) if query.doer else None     
                   
               list_owner_ratings.append(ListRatingSchema.model_validate( {
                "id":query.id,
                "job": job,
                "job_doer":doer,
                "job_owner":owner,
                "rating":query.rating,
                "rate_type":query.rate_type,
                "review_text":query.review_text,
                "created_at":query.created_at,
                "updated_at":query.updated_at 
                }))          
            elif query.rate_type.value == "DOER":
                count_doer += 1
                aggre_doer += query.rating
                job = SimpleJobSchema.model_validate({
                    "id": query.job.id,
                    "title": query.job.title,
                    "description": query.job.description,
                    "location": query.job.location,
                    "listed_price": query.job.listed_price,
                    "status": query.job.status,
                    "dateTimeCreated": query.job.dateTimeCreated,
                    "deleted": query.job.deleted,
                    }) if query.job else None
                owner = UserSchema.model_validate(query.owner) if query.owner else None
                doer = UserSchema.model_validate(query.doer) if query.doer else None 
                list_doer_ratings.append(ListRatingSchema.model_validate( {
                "id":query.id,
                "job": job,
                "job_doer":doer,
                "job_owner":owner,
                "rating":query.rating,
                "rate_type":query.rate_type,
                "review_text":query.review_text,
                "created_at":query.created_at,
                "updated_at":query.updated_at 
                }))
    
        return {
            "owner_ratings": list_owner_ratings,
            "doer_ratings": list_doer_ratings,
            "count_owner": count_owner,
            "count_doer": count_doer,
            "aggre_owner": aggre_owner,
            "aggre_doer": aggre_doer,}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Getting rating: {str(e)}"
        )
  


def list_all_rating(
    skip: int, 
    limit: int,
    db: Session,
    current_user: Users
):
    try:
        
        queries = (
                db.query(RatingModel)
                .options(
                    joinedload(RatingModel.job),
                    joinedload(RatingModel.owner),
                    joinedload(RatingModel.doer),
                )
                .offset(skip)
                .limit(limit)
                 .all()
            )
        
        if not queries:
            raise HTTPException(
                status_code=404,
                detail=f"Rating (skip={skip}, limit={limit}) not found"
            )
        list_ratings: List[ListRatingSchema] = []
        for query in queries:
            if not query:
                continue
            job = SimpleJobSchema.model_validate({
                "id": query.job.id,
                "title": query.job.title,
                "description": query.job.description,
                "location": query.job.location,
                "listed_price": query.job.listed_price,
                "status": query.job.status,
                "dateTimeCreated": query.job.dateTimeCreated,
                "deleted": query.job.deleted,
                }) if query.job else None
            owner = UserSchema.model_validate(query.owner) if query.owner else None
            doer = UserSchema.model_validate(query.doer) if query.doer else None
    
    
            list_ratings.append(ListRatingSchema.model_validate( {
            "id":query.id,
            "job": job,
            "job_doer":doer,
            "job_owner":owner,
            "rating":query.rating,
            "rate_type":query.rate_type,
            "review_text":query.review_text,
            "created_at":query.created_at,
            "updated_at":query.updated_at 
            }))
        return list_ratings
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Listing rating: {str(e)}"
        )



def list_owner_rating(
        skip: int, 
    limit: int,
    db: Session,
    current_user: Users
):
    try:
        
        queries = (
                db.query(RatingModel)
                .options(
                    joinedload(RatingModel.job),
                    joinedload(RatingModel.owner),
                    joinedload(RatingModel.doer),
                )
                .filter(RatingModel.rate_type == "OWNER")
                .offset(skip)
                .limit(limit)
                 .all()
            )
        
        if not queries:
            raise HTTPException(
                status_code=404,
                detail=f"Rating (skip={skip}, limit={limit}) not found"
            )
        list_ratings: List[ListRatingSchema] = []
        for query in queries:
            if not query:
                continue
            job = SimpleJobSchema.model_validate({
                "id": query.job.id,
                "title": query.job.title,
                "description": query.job.description,
                "location": query.job.location,
                "listed_price": query.job.listed_price,
                "status": query.job.status,
                "dateTimeCreated": query.job.dateTimeCreated,
                "deleted": query.job.deleted,
                }) if query.job else None
            owner = UserSchema.model_validate(query.owner) if query.owner else None
            doer = UserSchema.model_validate(query.doer) if query.doer else None
    
    
            list_ratings.append(ListRatingSchema.model_validate( {
            "id":query.id,
            "job": job,
            "job_doer":doer,
            "job_owner":owner,
            "rating":query.rating,
            "rate_type":query.rate_type,
            "review_text":query.review_text,
            "created_at":query.created_at,
            "updated_at":query.updated_at 
            }))
        return list_ratings
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Listing rating: {str(e)}"
        )


def list_doer_rating(
        skip: int, 
    limit: int,
    db: Session,
    current_user: Users
):
    try:
        
        queries = (
                db.query(RatingModel)
                .options(
                    joinedload(RatingModel.job),
                    joinedload(RatingModel.owner),
                    joinedload(RatingModel.doer),
                )
                .filter(RatingModel.rate_type == "DOER")
                .offset(skip)
                .limit(limit)
                 .all()
            )
        
        if not queries:
            raise HTTPException(
                status_code=404,
                detail=f"Rating (skip={skip}, limit={limit}) not found"
            )
        list_ratings: List[ListRatingSchema] = []
        for query in queries:
            if not query:
                continue
            job = SimpleJobSchema.model_validate({
                "id": query.job.id,
                "title": query.job.title,
                "description": query.job.description,
                "location": query.job.location,
                "listed_price": query.job.listed_price,
                "status": query.job.status,
                "dateTimeCreated": query.job.dateTimeCreated,
                "deleted": query.job.deleted,
                }) if query.job else None
            owner = UserSchema.model_validate(query.owner) if query.owner else None
            doer = UserSchema.model_validate(query.doer) if query.doer else None
    
    
            list_ratings.append(ListRatingSchema.model_validate( {
            "id":query.id,
            "job": job,
            "job_doer":doer,
            "job_owner":owner,
            "rating":query.rating,
            "rate_type":query.rate_type,
            "review_text":query.review_text,
            "created_at":query.created_at,
            "updated_at":query.updated_at 
            }))
        return list_ratings
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Listing rating: {str(e)}"
        )
