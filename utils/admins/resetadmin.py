from fastapi import HTTPException
from sqlalchemy.orm import Session 
from sqlalchemy import func
from models.accounts import Users, Admins, passResetTokens 
from schemas.general.resetPassword import ResetPassword 
from schemas.admins.admin import Admin
import hashlib
def ResetPasswordAdmin(payload: ResetPassword, db: Session ):  
   try:    
       db.begin()     
       ThisUser = db.query(Users).filter(func.trim(func.lower(Users.emailAddy)) == payload.emailAddy.strip().lower()).first() 
       if ThisUser is None:
            raise HTTPException(status_code=404, detail=f"Users(EmailAddy={payload.emailAddy}) does not exist in DB.")
       ThisAdmin = db.query(Admins).filter(Admins.user_id == ThisUser.id).first()
       if ThisAdmin is None:
            raise HTTPException(status_code=404, detail=f"Admin(EmailAddy={payload.emailAddy}) does not exist in DB.")
       if payload.password.strip() != payload.passwordConfirmed.strip():
            raise HTTPException(status_code=404, detail=f"Admin.passwords do not match.")
       ThisToken = db.query(passResetTokens).filter(passResetTokens.user_id == ThisUser.id).first()
       if ThisToken is None:
            raise HTTPException(status_code=404, detail=f"PasswordReset token does not exist in DB.")
       pToken = ThisToken.pToken # 10-digit number or token
       code = f"{pToken}{payload.emailAddy.strip().lower()}"
       code = hashlib.md5(code.encode()).hexdigest()
       if code != payload.eCode:
            raise HTTPException(status_code=404, detail=f"PasswordReset: Token does not match DB's.")      
       password = hashlib.md5(payload.password.encode()).hexdigest()   
       ThisUser.password = password
       db.add(ThisUser)
       db.flush()
       vTokens = db.query(passResetTokens).filter(passResetTokens.user_id == ThisUser.id).all()
       for Token in vTokens:
            db.delete(Token)     
       ret = Admin(id = ThisAdmin.id,username = ThisUser.username,  firstname =  ThisUser.firstname,  
                middlename = ThisUser.middlename, lastname = ThisUser.lastname,emailAddy = ThisUser.emailAddy, 
                dateCreated = ThisAdmin.dateTimeCreated, is_Active= ThisAdmin.is_Active)  
       db.commit() 
       sendResetPasswordSuccessMsg(pToken , payload)        
       return ret    
   except Exception as e: 
        db.rollback()        
        raise e  
def sendResetPasswordSuccessMsg(ten_digit:str,payload:ResetPassword):        
      from infrastructure.emailer  import  sendEmail   
      code = f"{ten_digit}{payload.emailAddy.strip().lower()}"
      code = hashlib.md5(code.encode()).hexdigest()
      retMsg =  sendEmail(subject="Password Reset: Success", 
                          message="Your password reset is successful", receiver_email= payload.emailAddy)