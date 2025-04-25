from fastapi import   HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.accounts import  Users,vTokens
from schemas.users.usercreate import UserCreate
from schemas.users.user import User #
def create_user(user: UserCreate, db: Session):  
    try:
        from .getuser import get_user_by_email_ver2
        Thisuser:User =  get_user_by_email_ver2(user.emailAddy, db)
        if Thisuser :  # record exists...do not create again
            raise HTTPException(status_code=404, detail=f"User(username={user.emailAddy}) exists in DB.") 
        from .getuser import get_user_ver2
        Thisuser:User =  get_user_ver2(user.username, db)     
        if Thisuser:  # record exists...do not create again    
            raise HTTPException(status_code=404, detail=f"User(username={user.username}) exists in DB.")         
        db.reset()
        db.begin()
        import hashlib, random
        ten_digit =  str(int(''.join(str(random.randint(0,9)) for _ in range(10)))) # email verification token
        password = hashlib.md5(user.password.strip().encode()).hexdigest()   
        db_user = Users(username = user.username, 
                        password = password, 
                        firstname = user.firstname, 
                        middlename = user.middlename,
                        lastname = user.lastname,
                        emailAddy = user.emailAddy) 
        db.add(db_user) 
        db.flush()  
        queryResult = db.query(Users, vTokens).join(vTokens, Users.id == vTokens.user_id)
        ThisUserAndTokens = queryResult.filter(func.lower(func.trim(Users.username)) == user.username.strip().lower()).first()
        if ThisUserAndTokens is None:
            # create verification token for this user           
            db_vToken = vTokens(emailVerificationToken = ten_digit, user_id = db_user.id) # inserts verification token 
            db.add(db_vToken) 
            db.flush()       
        db.commit() 
        return User( id= db_user.id, username = user.username,  firstname = user.firstname,  
                    middlename = user.middlename, lastname = user.lastname,emailAddy = user.emailAddy, 
                    dateCreated = db_user.dateTimeCreated )
    except Exception as e:
        db.rollback()
        raise e
def create_user_ver2(user: UserCreate, password:str, ten_digit:str, db: Session): 
    try:  # this method is invariably invoked inside an ATOMIC Transaction
        from .getuser import get_user_by_email_ver2
        Thisuser:User =  get_user_by_email_ver2(user.emailAddy, db)
        if Thisuser :  #  email exists in DB
            if Thisuser.username.lower().strip() != user.username.lower().strip():
                raise HTTPException(status_code=404, detail=f"User(username={user.username}) is taken")    
            else:
                ThisParticularUser:Users = db.query(Users).filter(func.lower(func.trim(Users.username)) == user.username.strip().lower()).first()
                import hashlib 
                if ThisParticularUser.password == hashlib.md5(password.strip().encode()).hexdigest():
                    return  Thisuser  # user is already created...return it to the caller 
                else:
                    raise HTTPException(status_code=404, detail=f"Existing User: User(password=(***)) not matching DB's")                
            from .getuser import get_user_ver2 
            Thisuser:User =  get_user_ver2(user.username, db)
            if Thisuser:  # username exists in DB
                if Thisuser.emailAddy.strip().lower() != user.emailAddy.strip().lower():
                    raise HTTPException(status_code=404, detail=f"User(emailAddy={user.emailAddy}) is taken") 
                else:
                    ThisParticularUser:Users = db.query(Users).filter(func.lower(func.trim(Users.username)) == user.username.strip().lower()).first()
                import hashlib 
                if ThisParticularUser.password == hashlib.md5(password.strip().encode()).hexdigest() :
                    return  Thisuser  # user is already created...return it to the caller 
                else:
                    raise HTTPException(status_code=404, detail=f"Existing User: User(password={user.password}) not matching DB's") 
        import hashlib        
        password = hashlib.md5(user.password.strip().encode()).hexdigest()   
        db_user = Users(username = user.username, 
                        password = password, 
                        firstname = user.firstname, 
                        middlename = user.middlename,
                        lastname = user.lastname,
                        emailAddy = user.emailAddy) # create a new User
        db.add(db_user) 
        db.flush()      
        queryResult = db.query(Users, vTokens).join(vTokens, Users.id == vTokens.user_id)
        ThisUserAndTokens = queryResult.filter(func.lower(func.trim(Users.username))== user.username.strip().lower()).first()       
        if ThisUserAndTokens is None:
            # create verification token for this user           
            db_vToken = vTokens(emailVerificationToken = ten_digit, user_id = db_user.id) # inserts verification token 
            db.add(db_vToken) 
            db.flush()        
        return User( id = db_user.id, username = user.username,  firstname = user.firstname,  
                    middlename = user.middlename, lastname = user.lastname,emailAddy = user.emailAddy, 
                    dateCreated = db_user.dateTimeCreated ) # returns the new user to the caller.
    except Exception as e:        
        raise e   