from .sendemail import  deliverEmail
from .configurations import key 
from cryptography.fernet import Fernet 
def sendEmail(optTypeOfUser = "0", 
    receiver_email = "adekunle.adekoya@easyshop.ng", code = "", uri = "",
    subject = "Account Verification", 
    message = "Kindly open the link below in a browser to verify your account",
    processor = ""
    ):
    sender_email = "adekunle.adekoya@easyshop.ng"   
    linkUsed2VerifyAccount = ""  
    ret = f"key: {key}"  
    try:         
        code = str(code)          
        bytedEmail =  f"{receiver_email}&{optTypeOfUser}".encode() #converts string to bytes
        f = Fernet(key)
        token = f.encrypt(bytedEmail)
        mi = token.decode()  #converts to string so as to fit into url string    
        if processor.strip()   != "":
            linkUsed2VerifyAccount = f"{uri}/{processor}/?is={code}&em={mi}"
        message = f"{message} <br> {linkUsed2VerifyAccount}"
        ret = deliverEmail(subject,sender_email, receiver_email, message )             
    except Exception as e:  
        ret = str(e) 
    return   ret

import re

def is_valid_email(email: str) -> bool:
    # Regular expression pattern to validate an email address
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Use re.match() to check if the email matches the pattern
    if re.match(email_regex, email):
        return True
    return False
