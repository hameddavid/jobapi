from fastapi import   HTTPException
from sqlalchemy.orm import Session
from models.accounts import Users 
from models.jobs import Rating as RatingModel
from schemas.general.deletion import SoftDeletion







def toggle_step_down_rating(rating_id: int, delStatus: SoftDeletion ,TheUser:Users, db: Session ):  
    try:
       rateObj = db.query(RatingModel).filter(RatingModel.id == rating_id).first()
       if rateObj is None:
           raise HTTPException(status_code=404, detail=f"Rating  with id {rating_id} not found.")
       if  "admin" not in TheUser.roles:
               # Check if the user is not the creator and is not an admin
           raise HTTPException(status_code=403, detail="You do not have permission to stepdown this rating.")
       
       rateObj.deleted = delStatus.value
       db.commit()
       db.refresh(rateObj)
       return rateObj
    except Exception as e:
        db.rollback()        
        raise HTTPException(status_code=404, detail=f"Toggling rating : {str(e)})") 