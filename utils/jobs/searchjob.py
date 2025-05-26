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
        query_string = text(
            """
            SELECT
                j.*,
                u_owner.id AS owner_id,
                u_owner.username AS owner_username, 
                u_owner.emailAddy AS owner_emailAddy,
                u_owner.firstname AS owner_firstname,
                u_owner.middlename AS owner_middlename,
                u_owner.lastname AS owner_lastname,
                u_owner.dateTimeCreated AS owner_dateTimeCreated,

                jc.id AS category_id,
                jc.name AS category_name, 
                jc.description AS category_description, 
                jc.deleted AS category_deleted, 
                jc.createdBy AS category_createdBy, 
                jc.updatedAt AS category_updatedAt,

                u_cat_user.id AS cat_user_id,
                u_cat_user.username AS cat_user_username,
                u_cat_user.emailAddy AS cat_user_emailAddy,
                u_cat_user.firstname AS cat_user_firstname,
                u_cat_user.middlename AS cat_user_middlename,
                u_cat_user.lastname AS cat_user_lastname,
                u_cat_user.dateTimeCreated AS cat_user_dateTimeCreated,
        

                MATCH(j.title, j.description, j.keywords) AGAINST(:query IN NATURAL LANGUAGE MODE) AS score
            FROM jobs j
            LEFT JOIN users u_owner ON j.user_id = u_owner.id
            LEFT JOIN jobCategory jc ON j.job_category_id = jc.id
            LEFT JOIN users u_cat_user ON jc.createdBy = u_cat_user.id 
            WHERE MATCH(j.title, j.description, j.keywords) AGAINST(:query IN NATURAL LANGUAGE MODE)
            ORDER BY score DESC
            """
        ).bindparams(query=q)
        
        results = db.execute(query_string).fetchall()
        print(f"Results: {results}")
        if not results:
            raise HTTPException(status_code=404, detail="No jobs found matching the search criteria.")
        
        job_list: List[ListJobSchema] = []
        for job in results:
            owner_data = UserSchema.model_validate({
                "id": job[12],
                "username": job[13],
                "emailAddy": job[14],
                "firstname": job[15],
                "middlename": job[16],
                "lastname": job[17],
                "dateTimeCreated": job[18],
            })
            cat_owner = UserSchema.model_validate({
                "id": job[25],
                "username": job[26],
                "emailAddy": job[27],
                "firstname": job[28],
                "middlename": job[29],
                "lastname": job[30],
                "dateTimeCreated": job[31],
                })  
            category_data = GetJobCategorySchema.model_validate({
                "id": job[19],
                "name": job[20],
                "description": job[21],
                "deleted": job[22],
                "createdBy": cat_owner,  
                "createdAt": job[23],
                "updatedAt": job[24],
            })
            this_job = ListJobSchema.model_validate({
                "id": job[0],
                "title": job[1],
                "description": job[2],
                "listed_price": job[8],
                "location": job[7],
                "owner": owner_data,
                "category": category_data,
                "dateTimeCreated": job[3],
                "status": job[11],
                "deleted": job[6],
            })
            job_list.append(this_job)
        return job_list

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"Listing jobs: {str(e)}")