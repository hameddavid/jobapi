from fastapi import   HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.accounts import Users, Admins, vTokens
from schemas.general.verifyemailaccount import VerifyEmailAccount 
from schemas.admins.admin import Admin
def verify_admin(payload: VerifyEmailAccount, db: Session ):  
   try:       
     emailAddy:str= payload.email
     eCode:str = payload.eCode  # is previously sent to inbox of admin after creating an account
     password:str = payload.password 
     queryResult = db.query(Users, Admins).join(Admins, Users.id == Admins.user_id)
     ThisUserAndAdmin = queryResult.filter(func.trim(func.lower(Users.emailAddy)) == emailAddy.strip().lower()).first() 
     if ThisUserAndAdmin is None:
        raise HTTPException(status_code=404, detail=f"Admin(email={emailAddy}) does not exist in DB.")
     Thisuser, ThisAdmin=  ThisUserAndAdmin  # unpacks  
     import hashlib         
     password = hashlib.md5(password.encode()).hexdigest()   
     if Thisuser.password != password:
         raise HTTPException(status_code=404, detail=f"Admin(password=***) does not match DB's.")
     # retrieve email verification token fron vTokens
     queryResult = db.query(Users, vTokens).join(vTokens, Users.id == vTokens.user_id)
     ThisUserAndTokens = queryResult.filter(func.trim(func.lower(Users.username)) == Thisuser.username.strip().lower()).first()
     if ThisUserAndTokens is None:
         raise HTTPException(status_code=404, detail=f"Admin's verification token is missing in DB.")
     _ , ThisToken = ThisUserAndTokens # unpacks object     
     code = f"{ThisToken.emailVerificationToken}{emailAddy.strip().lower()}"
     code = hashlib.md5(code.encode()).hexdigest()    
     if code != eCode:
        raise HTTPException(status_code=404, detail=f"Admin(eCode={eCode}) does not match DB's.")     
     Thisuser.isVerifiedEmail = True
     db.add(Thisuser)
     db.flush()  
     # proceed to delete the token from vTokens since it is already used for verification
     Tokens = db.query(vTokens).filter(vTokens.user_id == Thisuser.id ).all()
     for Token in Tokens:
        db.delete(Token)      
     ret = Admin(id = ThisAdmin.id,username = Thisuser.username,  firstname =  Thisuser.firstname,  
                middlename = Thisuser.middlename, lastname = Thisuser.lastname,emailAddy = Thisuser.emailAddy, 
                dateCreated = ThisAdmin.dateTimeCreated, is_Active= ThisAdmin.is_Active)     
     db.commit()
     return ret
   except Exception as e: 
        db.rollback()        
        raise e   
    
  