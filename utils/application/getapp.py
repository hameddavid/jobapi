from fastapi import   HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload
from typing import List
from schemas.users.user import User as UserSchema
from schemas.jobs.job import ListJobSchema
from schemas.apps.appschema import GetAppSchema
from models.applications import applications as appModel
from models.jobs import jobs as jobModel, jobCategory as JobCategoryModel
from schemas.jobs.jobCategorySchema import GetJobCategorySchema



def get_app_by_job_id(job_id: int,user: UserSchema,skip,limit, db: Session) -> GetAppSchema:
    try:
        # Eager loading of the user and job relationship
        appQ = (
            db.query(appModel)
            .options(joinedload(appModel.user),
                     joinedload(appModel.job).joinedload(jobModel.owner),
                     joinedload(appModel.job).joinedload(jobModel.job_category).joinedload(JobCategoryModel.user)
                     )
            .filter(appModel.deleted == 'N')
            .filter(appModel.job_id == job_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        if not appQ:
            raise HTTPException(status_code=404, detail=f"applications (skip={skip}, limit={limit}) not found")
        appList: List[GetAppSchema] = []
        for app in appQ:
            app_owner = UserSchema.model_validate(app.user)
            job_owner = UserSchema.model_validate(app.job.owner)
            cat_owner = UserSchema.model_validate(app.job.job_category.user)
            job_cat =  GetJobCategorySchema.model_validate({
                "id": app.job.job_category.id,
                "name": app.job.job_category.name,
                "description": app.job.job_category.description,
                "deleted": app.job.job_category.deleted,
                "createdBy": cat_owner,  
                "createdAt": app.job.job_category.createdAt,
                "updatedAt": app.job.job_category.updatedAt,
            })
            job = ListJobSchema.model_validate({
                "id": app.job.id,
                "title": app.job.title,
                "description": app.job.description,
                "listed_price": app.job.listed_price,
                "location": app.job.location,
                "owner": job_owner,
                "category": job_cat,
                "dateTimeCreated": app.job.dateTimeCreated,
                "status": app.job.status,
                "deleted": app.job.deleted,
            })
            apps = GetAppSchema.model_validate({
                "id": app.id,
                "title": app.title,
                "narration": app.narration,
                "doc_1": app.doc_1,
                "doc_2": app.doc_2,
                "doc_3": app.doc_3,
                "image": app.image,
                "suitable_price": app.suitable_price,
                "rejection_reason": app.rejection_reason,
                "job": job,
                "owner": app_owner,
                "status": app.status,
                "dateTimeCreated": app.dateTimeCreated,
                "dateTimeUpdated": app.dateTimeUpdated,
            })
            appList.append(apps)
        return appList
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"Listing applications : {str(e)})")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"Listing applications : {str(e)})")


def get_app_by_id(app_id: int,user: UserSchema, db: Session) -> GetAppSchema:
    try:
        appQ = (
            db.query(appModel)
            .options(joinedload(appModel.user),
                     joinedload(appModel.job).joinedload(jobModel.owner),
                     joinedload(appModel.job).joinedload(jobModel.job_category).joinedload(JobCategoryModel.user)
                     )
            .filter(appModel.id == app_id)
            .first()
        )
        if not appQ:
            raise HTTPException(status_code=404, detail=f"application with id {app_id} not found")
        if appQ.user_id != user.id and "admin" not in user.roles:
            # Check if the user is not the creator and is not an admin
            raise HTTPException(status_code=403, detail="You do not have permission to view this application.")
        
        app_owner = UserSchema.model_validate(appQ.user)
        job_owner = UserSchema.model_validate(appQ.job.owner)
        cat_owner = UserSchema.model_validate(appQ.job.job_category.user)
        job_cat =  GetJobCategorySchema.model_validate({
            "id": appQ.job.job_category.id,
            "name": appQ.job.job_category.name,
            "description": appQ.job.job_category.description,
            "deleted": appQ.job.job_category.deleted,
            "createdBy": cat_owner,  
            "createdAt": appQ.job.job_category.createdAt,
            "updatedAt": appQ.job.job_category.updatedAt,
        })
        job = ListJobSchema.model_validate({
            "id": appQ.job.id,
            "title": appQ.job.title,
            "description": appQ.job.description,
            "listed_price": appQ.job.listed_price,
            "location": appQ.job.location,
            "owner": job_owner,
            "category": job_cat,
            "dateTimeCreated": appQ.job.dateTimeCreated,
            "status": appQ.job.status,
            "deleted": appQ.job.deleted,
        })
        apps = GetAppSchema.model_validate({
            "id": appQ.id,
            "title": appQ.title,
            "narration": appQ.narration,
            "doc_1": appQ.doc_1,
            "doc_2": appQ.doc_2,
            "doc_3": appQ.doc_3,
            "image": appQ.image,
            "suitable_price": appQ.suitable_price,
            "rejection_reason": appQ.rejection_reason,
            "job": job,
            "owner": app_owner,
            "status": appQ.status,
            "dateTimeCreated": appQ.dateTimeCreated,
            "dateTimeUpdated": appQ.dateTimeUpdated,
        })
        return apps
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"Getting application : {str(e)})")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"Getting application : {str(e)})")


def list_my_apps(user: UserSchema, skip: int, limit: int, db: Session) -> List[GetAppSchema]:
    try:
        # Eager loading of the user and job relationship
        appQ = (
            db.query(appModel)
            .options(joinedload(appModel.user),
                     joinedload(appModel.job).joinedload(jobModel.owner),
                     joinedload(appModel.job).joinedload(jobModel.job_category).joinedload(JobCategoryModel.user)
                     )
            .filter(appModel.deleted == 'N')
            .filter(appModel.user_id == user.id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        if not appQ:
            raise HTTPException(status_code=404, detail=f"applications (skip={skip}, limit={limit}) not found")
        appList: List[GetAppSchema] = []
        for app in appQ:
            app_owner = UserSchema.model_validate(app.user)
            job_owner = UserSchema.model_validate(app.job.owner)
            cat_owner = UserSchema.model_validate(app.job.job_category.user)
            job_cat =  GetJobCategorySchema.model_validate({
                "id": app.job.job_category.id,
                "name": app.job.job_category.name,
                "description": app.job.job_category.description,
                "deleted": app.job.job_category.deleted,
                "createdBy": cat_owner,  
                "createdAt": app.job.job_category.createdAt,
                "updatedAt": app.job.job_category.updatedAt,
            })
            job = ListJobSchema.model_validate({
                "id": app.job.id,
                "title": app.job.title,
                "description": app.job.description,
                "listed_price": app.job.listed_price,
                "location": app.job.location,
                "owner": job_owner,
                "category": job_cat,
                "dateTimeCreated": app.job.dateTimeCreated,
                "status": app.job.status,
                "deleted": app.job.deleted,
            })
            apps = GetAppSchema.model_validate({
                "id": app.id,
                "title": app.title,
                "narration": app.narration,
                "doc_1": app.doc_1,
                "doc_2": app.doc_2,
                "doc_3": app.doc_3,
                "image": app.image,
                "suitable_price": app.suitable_price,
                "rejection_reason": app.rejection_reason,
                "job": job,
                "owner": app_owner,
                "status": app.status,
                "dateTimeCreated": app.dateTimeCreated,
                "dateTimeUpdated": app.dateTimeUpdated,
            })
            appList.append(apps)
        return appList
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"Listing applications : {str(e)})")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"Listing applications : {str(e)})")


def list_user_apps_by_admin(user_id: int, skip: int, limit: int, db: Session) -> List[GetAppSchema]:
    try:
        # Eager loading of the user and job relationship
        appQ = (
            db.query(appModel)
            .options(joinedload(appModel.user),
                     joinedload(appModel.job).joinedload(jobModel.owner),
                     joinedload(appModel.job).joinedload(jobModel.job_category).joinedload(JobCategoryModel.user)
                     )
            .filter(appModel.deleted == 'N')
            .filter(appModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        if not appQ:
            raise HTTPException(status_code=404, detail=f"applications (skip={skip}, limit={limit}) not found")
        appList: List[GetAppSchema] = []
        for app in appQ:
            app_owner = UserSchema.model_validate(app.user)
            job_owner = UserSchema.model_validate(app.job.owner)
            cat_owner = UserSchema.model_validate(app.job.job_category.user)
            job_cat =  GetJobCategorySchema.model_validate({
                "id": app.job.job_category.id,
                "name": app.job.job_category.name,
                "description": app.job.job_category.description,
                "deleted": app.job.job_category.deleted,
                "createdBy": cat_owner,  
                "createdAt": app.job.job_category.createdAt,
                "updatedAt": app.job.job_category.updatedAt,
            })
            job = ListJobSchema.model_validate({
                "id": app.job.id,
                "title": app.job.title,
                "description": app.job.description,
                "listed_price": app.job.listed_price,
                "location": app.job.location,
                "owner": job_owner,
                "category": job_cat,
                "dateTimeCreated": app.job.dateTimeCreated,
                "status": app.job.status,
                "deleted": app.job.deleted,
            })
            apps = GetAppSchema.model_validate({
                "id": app.id,
                "title": app.title,
                "narration": app.narration,
                "doc_1": app.doc_1,
                "doc_2": app.doc_2,
                "doc_3": app.doc_3,
                "image": app.image,
                "suitable_price": app.suitable_price,
                "rejection_reason": app.rejection_reason,
                "job": job,
                "owner": app_owner,
                "status": app.status,
                "dateTimeCreated": app.dateTimeCreated,
                "dateTimeUpdated": app.dateTimeUpdated,
            })
            appList.append(apps)
        return appList
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"Listing applications : {str(e)})")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=f"Listing applications : {str(e)})")


def list_apps(skip: int, limit: int, db: Session) -> List[GetAppSchema]:
    try:
        # Eager loading of the user and job relationship
        appQ = (
            db.query(appModel)
            .options(joinedload(appModel.user),
                     joinedload(appModel.job).joinedload(jobModel.owner),
                     joinedload(appModel.job).joinedload(jobModel.job_category).joinedload(JobCategoryModel.user)
                     )
            .filter(appModel.deleted == 'N')
            .offset(skip)
            .limit(limit)
            .all()
        )
        if not appQ:
            raise HTTPException(status_code=404, detail=f"applications (skip={skip}, limit={limit}) not found")
        appList: List[GetAppSchema] = []
        for app in appQ:
            app_owner = UserSchema.model_validate(app.user)
            job_owner = UserSchema.model_validate(app.job.owner)
            cat_owner = UserSchema.model_validate(app.job.job_category.user)   
            job_cat =  GetJobCategorySchema.model_validate({
                "id": app.job.job_category.id,
                "name": app.job.job_category.name,
                "description": app.job.job_category.description,
                "deleted": app.job.job_category.deleted,
                "createdBy": cat_owner,  
                "createdAt": app.job.job_category.createdAt,
                "updatedAt": app.job.job_category.updatedAt,
            })
            job = ListJobSchema.model_validate({
                "id": app.job.id,
                "title": app.job.title,
                "description": app.job.description,
                "listed_price": app.job.listed_price,
                "location": app.job.location,
                "owner": job_owner,
                "category": job_cat,
                "dateTimeCreated": app.job.dateTimeCreated,
                "status": app.job.status,
                "deleted": app.job.deleted,
            })
            apps = GetAppSchema.model_validate({
                "id": app.id,
                "title": app.title,
                "narration": app.narration,
                "doc_1": app.doc_1,
                "doc_2": app.doc_2,
                "doc_3": app.doc_3,
                "image": app.image,
                "suitable_price": app.suitable_price,
                "rejection_reason": app.rejection_reason,
                "job": job,
                "owner": app_owner,
                "status": app.status,
                "dateTimeCreated": app.dateTimeCreated,
                "dateTimeUpdated": app.dateTimeUpdated,
            })
            appList.append(apps)
        return appList
    except Exception as e:       
        raise HTTPException(status_code=404, detail=f"Error listing applications : {str(e)})") 
