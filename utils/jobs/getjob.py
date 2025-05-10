from models.jobs import jobs as jobModel, jobCategory as JobCategoryModel
from schemas.jobs.job import ListJobSchema
from schemas.jobs.jobCategorySchema import GetJobCategorySchema
from schemas.users.user import User as UserSchema
from typing import List, Optional
from datetime import datetime
from sqlalchemy import func
from fastapi import Query

from fastapi import   HTTPException
from sqlalchemy.orm import Session, joinedload



def list_jobs(skip: int, limit: int, db: Session) -> List[ListJobSchema]:
 
    try:
        # Eagerly load the 'owner' and 'job_category' relationships, and 'job_category.user'
        job_query = (
            db.query(jobModel)
            .options(
                joinedload(jobModel.owner),
                joinedload(jobModel.job_category).joinedload(JobCategoryModel.user) # Eager load user of category
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

        if not job_query:
            raise HTTPException(status_code=404, detail=f"Jobs (skip={skip}, limit={limit}) not found")

        job_list: List[ListJobSchema] = []
        for job in job_query:
            owner_data = UserSchema.model_validate(job.owner)
            cat_owner = UserSchema.model_validate(job.job_category.user)  # Eagerly loaded user of category
            category_data = GetJobCategorySchema.model_validate({
                "id": job.job_category.id,
                "name": job.job_category.name,
                "description": job.job_category.description,
                "deleted": job.job_category.deleted,
                "createdBy": cat_owner,  
                "createdAt": job.job_category.createdAt,
                "updatedAt": job.job_category.updatedAt,
            })
            this_job = ListJobSchema.model_validate({
                "id": job.id,
                "title": job.title,
                "description": job.description,
                "listed_price": job.listed_price,
                "location": job.location,
                "owner": owner_data,
                "category": category_data,
                "dateTimeCreated": job.dateTimeCreated,
                "status": job.status,
                "deleted": job.deleted,
            })
            job_list.append(this_job)
        return job_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing jobs: {str(e)}")




def get_job_by_id(job_id: int, db: Session) -> ListJobSchema:
    try:
        # Query the job by ID and eagerly load relationships
        job = (
            db.query(jobModel)
            .options(
                joinedload(jobModel.owner),
                joinedload(jobModel.job_category).joinedload(JobCategoryModel.user)
            )
            .filter(jobModel.id == job_id)
            .first()
        )

        if not job:
            raise HTTPException(status_code=404, detail=f"Job with ID {job_id} not found")

        # Validate and serialize the owner data
        owner_data = UserSchema.model_validate(job.owner)

        # Validate and serialize the category data
        cat_owner = UserSchema.model_validate(job.job_category.user)
        category_data = GetJobCategorySchema.model_validate({
            "id": job.job_category.id,
            "name": job.job_category.name,
            "description": job.job_category.description,
            "deleted": job.job_category.deleted,
            "createdBy": cat_owner,
            "createdAt": job.job_category.createdAt,
            "updatedAt": job.job_category.updatedAt,
        })

        # Validate and serialize the job data
        job_data = ListJobSchema.model_validate({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "listed_price": job.listed_price,
            "location": job.location,
            "owner": owner_data,
            "category": category_data,
            "dateTimeCreated": job.dateTimeCreated,
            "status": job.status,
            "deleted": job.deleted,
        })

        return job_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving job: {str(e)}")
    
    
    
    


def list_jobs_with_filters(
    db: Session,
    skip: int = Query(0, ge=0,),
    limit: int = Query(50, ge=1,),
    category_id: Optional[int] = None,
    owner_id: Optional[int] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    job_name: Optional[str] = None,
    location: Optional[str] = None,
    job_description: Optional[str] = None,
) -> list[ListJobSchema]:
    try:
        # Base query with eager loading
        query = (
            db.query(jobModel)
            .options(
                joinedload(jobModel.owner),
                joinedload(jobModel.job_category).joinedload(JobCategoryModel.user)
            )
        )

        # Apply filters dynamically
        if category_id:
            query = query.filter(jobModel.job_category_id == category_id)
        if owner_id:
            query = query.filter(jobModel.owner_id == owner_id)
        if date_from:
            query = query.filter(jobModel.dateTimeCreated >= date_from)
        if date_to:
            query = query.filter(jobModel.dateTimeCreated <= date_to)
        if job_name:
            query = query.filter(func.lower(jobModel.title).contains(job_name.lower()))
        if location:
            query = query.filter(func.lower(jobModel.location).contains(location.lower()))
        if job_description:
            query = query.filter(func.lower(jobModel.description).contains(job_description.lower()))

        # Apply pagination
        jobs = query.offset(skip).limit(limit).all()

        if not jobs:
            raise HTTPException(status_code=404, detail="No jobs found with the given filters")

        # Serialize the results
        job_list = []
        for job in jobs:
            owner_data = UserSchema.model_validate(job.owner)
            cat_owner = UserSchema.model_validate(job.job_category.user)
            category_data = GetJobCategorySchema.model_validate({
                "id": job.job_category.id,
                "name": job.job_category.name,
                "description": job.job_category.description,
                "deleted": job.job_category.deleted,
                "createdBy": cat_owner,
                "createdAt": job.job_category.createdAt,
                "updatedAt": job.job_category.updatedAt,
            })
            this_job = ListJobSchema.model_validate({
                "id": job.id,
                "title": job.title,
                "description": job.description,
                "listed_price": job.listed_price,
                "location": job.location,
                "owner": owner_data,
                "category": category_data,
                "dateTimeCreated": job.dateTimeCreated,
                "status": job.status,
                "deleted": job.deleted,
            })
            job_list.append(this_job)

        return job_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing jobs with filters: {str(e)}")