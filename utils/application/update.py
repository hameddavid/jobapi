from fastapi import   HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from schemas.users.user import User
from schemas.apps.appschema import UpdateAppSchema
from models.applications import applications as appModel,AppStatus
from datetime import datetime 


def update_app(appData: UpdateAppSchema, ThisUser:User, db: Session ):  
    try:
        getApp = db.query(appModel).filter(appModel.id == appData.id).first()
        if getApp is None:
            raise HTTPException(status_code=404, detail=f"application with id {appData.id} not found or.")
        else:
            if getApp.user_id != ThisUser.id and "admin" not in ThisUser.roles:
                # Check if the user is not the creator and is not an admin
                raise HTTPException(status_code=403, detail="You do not have permission to update this application.")
            if appData.title is not None:
                getApp.title = appData.title 
            if appData.narration is not None:
                getApp.narration = appData.narration  
            if appData.doc_1 is not None: 
                    getApp.doc_1 = appData.doc_1  
            if appData.doc_2 is not None:
                   getApp.doc_2 = appData.doc_2
            if appData.doc_3 is not None:
                   getApp.doc_3 = appData.doc_3  
            if appData.image is not None:
                   getApp.image = appData.image
            if appData.suitable_price is not None:
                   getApp.suitable_price = appData.suitable_price                             
            getApp.dateTimeUpdated = datetime.utcnow() 
            db.commit()
            db.refresh(getApp)
            return getApp
    except Exception as e:       
        raise HTTPException(status_code=404, detail=f"Error updating application : {str(e)})") 
    


# update application by owner or admin

def update_app_status_by_owner_or_admin(appId: int,newStatus: AppStatus, TheUser:User, db: Session ):  
    try:
        appQ = db.query(appModel).filter(appModel.id == appId).first()
        if appQ is None:
            raise HTTPException(status_code=404, detail=f"Application with id {appId} not found.")
        else:
            if appQ.user_id != TheUser.id and "admin" not in TheUser.roles:
                # Check if the user is not the creator and is not an admin
                raise HTTPException(status_code=403, detail="You do not have permission to update this application.")
            appQ.status = newStatus
            appQ.dateTimeUpdated = datetime.utcnow()
            db.commit()
            db.refresh(appQ)
            return appQ
    except Exception as e:       
        raise HTTPException(status_code=404, detail=f"Error updating application: {str(e)})")
    