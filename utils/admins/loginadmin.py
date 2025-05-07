from fastapi import HTTPException 
from sqlalchemy.orm import Session 
from sqlalchemy import func
from models.accounts import Users, Admins 
from schemas.general.login import   LoginAdmin
from schemas.admins.admin import Admin, AdminAUTH
import hashlib
def LoginAdmin(payload: LoginAdmin, db: Session ):  
   try:   
       '''   
       placeHolderLabel = "username" 
       placeHolderValue = ""
       if payload.username.strip().lower() !=  "":  # login with username 
        ThisUser = db.query(Users).filter(func.lower(func.trim(Users.username)) == payload.username.strip().lower()).first()  
        placeHolderValue = payload.username  
       else:  # login with email address
       '''
       ThisUser = db.query(Users).filter(func.lower(func.trim(Users.emailAddy)) == payload.emailAddy.strip().lower()).first()
       placeHolderLabel = "emailAddy" 
       placeHolderValue = payload.emailAddy
       if ThisUser is None: 
            raise HTTPException(status_code=404, detail=f"User({placeHolderLabel}={placeHolderValue}) does not exist in DB.") 
       password = hashlib.md5(payload.password.strip().encode()).hexdigest()            
       if ThisUser.password != password:
           raise HTTPException(status_code=404, detail=f"User({placeHolderLabel}={placeHolderValue})'s password does not match DB's.")
       queryResult = db.query(Users, Admins).join(Admins, Users.id == Admins.user_id)
       ThisUserAndAdmin = queryResult.filter(Users.id == ThisUser.id).first() 
       if ThisUser.isVerifiedEmail is False:          
            if ThisUserAndAdmin is None:
                raise HTTPException(status_code=404, detail=f"Admin({placeHolderLabel}={placeHolderValue}) does not exist in DB.")      
            from models.accounts import vTokens
            Token = db.query(vTokens).filter(vTokens.user_id == ThisUser.id).first()
            if  Token is None:                    
                    import random
                    ten_digit =  str(int(''.join(str(random.randint(0,9)) for _ in range(10)))) # email verification token
                    db_vToken = vTokens(emailVerificationToken = ten_digit, user_id = ThisUser.id) # inserts verification token 
                    db.add(db_vToken) 
                    db.commit()
            else: # unused token exists for ThisUser...resuse                
                ten_digit =  Token.emailVerificationToken
            sendVerificationCodeToAdmin(ten_digit, payload)   
            raise HTTPException(status_code=404, detail=f"Admin({placeHolderLabel}={placeHolderValue}) account is awaiting verification...check your inbox.") 
       _ , ThisAdmin =   ThisUserAndAdmin
       if not ThisAdmin.is_Active:
           raise HTTPException(status_code=404, detail=f"Admin({placeHolderLabel}={placeHolderValue}) account requires activation by ADMIN.") 
       from utils.general.authentication import   create_access_token
       from utils.general.authentication import Token, timedelta 
       ACCESS_TOKEN_EXPIRE_MINUTES = 60  # Set token expiration to 1 hour
       access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
       access_token = create_access_token(
        data={"sub": ThisUser.username}, expires_delta=access_token_expires
          )       
       thisAdmin = Admin(id = ThisAdmin.id,  username = ThisUser.username,  firstname = ThisUser.firstname,  
                        middlename = ThisUser.middlename, lastname = ThisUser.lastname,emailAddy = ThisUser.emailAddy, 
                        dateCreated = ThisAdmin.dateTimeCreated, is_Active= ThisAdmin.is_Active) 
       return AdminAUTH(admin = thisAdmin,
                        token = access_token)    
   except Exception as e: 
        db.rollback()        
        raise e
def sendVerificationCodeToAdmin(ten_digit:str,payload:LoginAdmin):        
      from infrastructure.emailer  import  sendEmail   
      code = f"{ten_digit}{payload.emailAddy.strip().lower()}"
      code = hashlib.md5(code.encode()).hexdigest()
      sendEmail(processor =  payload.processor, subject="Verify Admin",
                          message="Please use the link below to verify your email account", 
                          receiver_email= payload.emailAddy, code = code, uri = payload.frontendURL)