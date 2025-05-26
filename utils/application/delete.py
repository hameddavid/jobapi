
from fastapi import   HTTPException
from sqlalchemy.orm import Session
from schemas.users.user import User
from schemas.general.deletion import SoftDeletion
from models.applications import applications as appModel



def delete_application(app_id: int, TheUser: User, db: Session ):  
    try:
        app = db.query(appModel).filter(appModel.id == app_id).first()
        if app is None:
            raise HTTPException(status_code=404, detail=f"Application with id {app_id} not found or does not belong to the user.")
        if app.user_id != TheUser.id and "admin" not in TheUser.roles:
            # Check if the user is not the creator and is not an admin
            raise HTTPException(status_code=403, detail="You do not have permission to delete this application.")
        if app.status.value != 'SUBMITTED':
            # Check if the application is not in the submitted state
            raise HTTPException(status_code=400, detail=f"Cannot delete application because its status has already changed from SUBMITTED to  {app.status.value}.")
        db.delete(app)
        db.commit()
        return {"detail": "Application deleted successfully"}
    except Exception as e:
        db.rollback()        
        raise HTTPException(status_code=404, detail=f"Deleting application : {str(e)})")




def soft_delete_application(app_id: int, delStatus:SoftDeletion, TheUser: User, db: Session ):  
    try:
        app = db.query(appModel).filter(appModel.id == app_id).first()
        if app is None:
            raise HTTPException(status_code=404, detail=f"Application with id {app_id} not found or does not belong to the user.")
        if "admin" not in TheUser.roles:
            # Check if the user is not the creator and is not an admin
            raise HTTPException(status_code=403, detail="You do not have permission to delete this application.")
        if app.status.value != 'SUBMITTED':
            # Check if the application is not in the submitted state
            raise HTTPException(status_code=400, detail=f"Cannot delete application because its status has already changed from SUBMITTED to  {app.status.value}.")
        app.deleted = delStatus.value
        db.commit()
        db.refresh(app)
        return {"detail": "Application soft deleted successfully"}
    except Exception as e:
        db.rollback()        
        raise HTTPException(status_code=404, detail=f"Deleting application : {str(e)})")