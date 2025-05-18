from fastapi import   HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from schemas.users.user import User
from schemas.apps.appschema import CreateAppSchema
from models.applications import applications as appModel
from models.jobs import jobs as jobModel



def create_app(appData: CreateAppSchema, ThisUser:User, db: Session ):  
    try:
        # check if the job is still available
        job = db.query(jobModel).filter(jobModel.id == appData.job_id).first()
        if not job or job.deleted == 'Y' or job.status != 'OPEN':
            raise HTTPException(status_code=404, detail="Job not available.")
        newApp = appModel(
          title = str(appData.title).capitalize(),
          narration = str(appData.narration).capitalize(),
          doc_1 = appData.doc_1,
          doc_2 = appData.doc_2,
          doc_3 = appData.doc_3,
          image = appData.image,
          suitable_price = appData.suitable_price,
          job_id = appData.job_id,
          user_id = ThisUser.id
        )
        db.add(newApp)
        db.commit()
        db.refresh(newApp)
        return newApp
    except IntegrityError as e:
        if "Duplicate entry" in str(e) and "'unique_user_per_job'" in str(e):
            raise HTTPException(
                status_code=400,
                detail="You have already applied for this job."
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Error creating application: {str(e)}"
            )    
    except Exception as e:       
        raise HTTPException(status_code=404, detail=f"Creating application : {str(e)})") 
    
