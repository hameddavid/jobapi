from fastapi import  Depends,Query
from sqlalchemy.orm import Session 
from utils.jobs.searchjob import search_job
from models.database import  get_db
from schemas.jobs.job import ListJobSchema 
from schemas.users.user import User
from utils.general.authentication import get_current_user
from .router import router


from sqlalchemy import func,text
from models.jobs import jobs as jobModel

@router.get("/search_job_full_text", include_in_schema=True, response_model="")
def do(q: str = Query(..., min_length=3),
                    db: Session = Depends(get_db),TheUser: User = Depends(get_current_user)):  
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
            u_owner.roles AS owner_roles,

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
            u_cat_user.roles AS cat_user_roles,

            MATCH(j.title, j.description, j.keywords) AGAINST(:query IN NATURAL LANGUAGE MODE) AS score
        FROM jobs j
        LEFT JOIN users u_owner ON j.owner_id = u_owner.id
        LEFT JOIN jobCategory jc ON j.category_id = jc.id
        LEFT JOIN users u_cat_user ON jc.user_id = u_cat_user.id 
        WHERE MATCH(j.title, j.description, j.keywords) AGAINST(:query IN NATURAL LANGUAGE MODE)
        ORDER BY score DESC
        """
    ).bindparams(query=q)
     
    result = db.execute(query_string).fetchall()
    print("Raw SQL full-text query executed successfully:", result)
    return {"raw_sql_test": "success", "results": [row[0] for row in result]}
    query = (db.query(
            jobModel,
            func.match(jobModel.title, jobModel.description, jobModel.keywords)
            .against(q).label("score")
            
        )
        .filter(func.match(jobModel.title, jobModel.description, jobModel.keywords)
            .against(q))
        .order_by(text("score DESC"))
                
     )
    
    query =  query.all()
    return {"raw_sql_test": "success", "results": [row[0] for row in query]}
    # return search_job(q, db)