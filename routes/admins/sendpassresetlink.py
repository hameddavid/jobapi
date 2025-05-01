from fastapi import   HTTPException
from sqlalchemy.orm import Session 
from sqlalchemy import func
from models.accounts import Users, passResetTokens 
from schemas.general.sendpasswordresetlink import SendPassResetLink 
import hashlib, random
def SendLink(payload: SendPassResetLink, db: Session ):  
   try:   
       emailAddy:str = payload.emailAddy
       ThisUser = db.query(Users).filter(func.trim(func.lower(Users.emailAddy)) == emailAddy.strip().lower()).first()  
       if ThisUser is None:
           raise HTTPException(status_code=404, detail=f"Operator(emailAddy={payload.emailAddy}) does not exist in DB.") 
       vTokens = db.query(passResetTokens).filter(Users.id == ThisUser.id).first()       
       if vTokens is None:  # create Token           
           ten_digit =  str(int(''.join(str(random.randint(0,9)) for _ in range(10)))) # password reset token
           vTokens = passResetTokens(pToken = ten_digit, user_id = ThisUser.id) # inserts  token in DB
           db.add(vTokens) 
           db.flush()   
           db.commit()    
       vToken = vTokens.pToken   # retrieves the 10-digit token
       sendPasswordResetLinkToOperator(vToken, payload)
       raise HTTPException(status_code=200, detail=f"Operator.sendPassResetLink(Token={vToken})")      
   except Exception as e: 
        db.rollback()        
        raise e  
def sendPasswordResetLinkToOperator(ten_digit:str,payload:SendPassResetLink):        
      from infrastructure.emailer  import  sendEmail   
      code = f"{ten_digit}{payload.emailAddy.strip().lower()}"
      code = hashlib.md5(code.encode()).hexdigest()
      retMsg =  sendEmail(processor = payload.processor, subject = "Password Reset: BioAPP", 
                          message="Kindly use the link below to reset your password",  receiver_email= payload.emailAddy,  code = code, uri = payload.frontendURL)