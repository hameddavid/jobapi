# routers/ratings.py

from fastapi import   HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.accounts import Users 
from models.jobs import jobs
from models.jobs import Rating as RatingModel
from schemas.jobs.rating import RatingCreateSchema




def create_rating_for_job_owner(
    rating_data: RatingCreateSchema ,
    db: Session ,
    current_user: Users 
):
    try:
        # 1. Validate Job Existence
        job = db.execute(select(jobs).where(jobs.id == rating_data.job_id)).scalar_one_or_none()
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

        # 2. Validate Job Owner ID (ensure it's the actual owner of the job)
        if job.user_id != rating_data.job_owner_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Provided job_owner_id does not match the actual owner of this job.")

        # 3. Validate current_user (job doer) has completed this job
        # This requires an application from current_user for this job with a 'Completed' status
        if job.status.value != 'COMPLETED':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must have completed this job to rate its owner."
            )

        # 4. Check if job doer has already rated this owner for this job
        existing_rating = db.execute(
            select(RatingModel)
            .where(
                RatingModel.job_doer_id == current_user.id,
                RatingModel.job_id == rating_data.job_id
            )
        ).scalar_one_or_none()

        if existing_rating:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already rated this job owner for this specific job."
            )

        # 5. Create the rating record
        db_rating = RatingModel(
            job_id=rating_data.job_id,
            job_doer_id=current_user.id,
            job_owner_id=rating_data.job_owner_id,
            rating=rating_data.rating,
            rate_type='OWNER',  
            review_text=rating_data.review_text
        )
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)

        return db_rating

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )
        
        



# 
def create_rating_for_job_doer(
    rating_data: RatingCreateSchema ,
    db: Session ,
    current_user: Users 
):
    try:
        # 1. Validate Job Existence
        job = db.execute(select(jobs).where(jobs.id == rating_data.job_id)).scalar_one_or_none()
        if not job:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

        # 2. Validate current_user is the actual owner of the job
        if job.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not the owner of this job.")

        # 3. Validate current_user (job doer) has completed this job
        # This requires an application from current_user for this job with a 'Completed' status
        if job.status.value != 'COMPLETED':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must have completed this job to rate its owner."
            )

        # 4. Check if job doer has already rated this owner for this job
        existing_rating = db.execute(
            select(RatingModel)
            .where(
                RatingModel.job_doer_id == current_user.id,
                RatingModel.job_id == rating_data.job_id
            )
        ).scalar_one_or_none()

        if existing_rating:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already rated this job owner for this specific job."
            )

        # 5. Create the rating record
        db_rating = RatingModel(
            job_id=rating_data.job_id,
            job_doer_id=current_user.id,
            job_owner_id=rating_data.job_owner_id,
            rating=rating_data.rating,
            rate_type='DOER',
            review_text=rating_data.review_text
        )
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)

        return db_rating

    except HTTPException as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )
        