from models.jobs import jobs as jobModel, jobCategory as JobCategoryModel
from schemas.jobs.job import ListJobSchema
from schemas.jobs.jobCategorySchema import GetJobCategorySchema
from schemas.users.user import User as UserSchema
from typing import List
from sqlalchemy import func,text

from fastapi import   HTTPException
from sqlalchemy.orm import Session, joinedload


def search_job(q: str ,db: Session) -> List[ListJobSchema]:
    # try:
        # job_query =  func.match(jobModel.title, jobModel.description, jobModel.keywords)
        # against_clause = job_query.against(q)

        # query = db.query(
        #     jobModel,
        #     against_clause.label("score"),
        # ).filter(
        #     against_clause
        # ).order_by(
        #     text("score DESC")
        # ).options(
        #     joinedload(jobModel.owner),
        #     joinedload(jobModel.job_category).joinedload(JobCategoryModel.user)
        # )
        
        query = (db.query(
            jobModel,
            func.match(jobModel.title, jobModel.description, jobModel.keywords)
            .against(q).label("score")
            
        )
        .filter(func.match(jobModel.title, jobModel.description, jobModel.keywords)
            .against(q))
        .order_by(text("score DESC"))
                
     )

        results = query.all()
        
        if not results:
            raise HTTPException(status_code=404, detail="No jobs found matching the search criteria.")
        
        job_list: List[ListJobSchema] = []
        for job in results:
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

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Listing jobs: {str(e)}")