def deliverEmail(subject = "None", 
    sender_email = "adekunle.adekoya@easyshop.ng", 
    receiver_email = "adekunleadekoya@gmail.com", msgToSend = "N/A"):     
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    try:
        # Email content
        message = MIMEMultipart()
        smtp_server = "mail.easyshop.ng"        
        sender_email = "no-replies@easyshop.ng"
        password = "5qJmZ9l]*OU%" 
        message['From'] =  sender_email
        message['To'] =  receiver_email
        message['Subject'] =  subject     
        body =  f"<html><body>{msgToSend}</body></html>"
        mime_type = 'html' 
        # Attach the body with the specified MIME type
        message.attach(MIMEText(body, mime_type))       
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP_SSL(smtp_server, 465)         
        server.login(sender_email, password)
        server.send_message(message) 
        errorMsgIfAny = "sent"        
    except Exception as e:
        errorMsgIfAny  =  str(e)  
    return    errorMsgIfAny


    '''

    return ;
    import smtplib  
    import email.message  
    msg = email.message.Message()
    errorMsgIfAny = "" 
    
    
    sender_email = "adekunleadekoya@gmail.com"
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls 
    password =  "vosuycqrmnmhzcpt" 
      
    smtp_server = "mail.easyshop.ng"
    port = 587  # For starttls 
    password =  "EasyTech123!" 
    sender_email = "no-replies@easyshop.ng"
    password = "5qJmZ9l]*OU%"
    
    try:
        msg = email.message.Message()
        msg['Subject'] =  subject         
        msg.add_header('Content-Type','text/html')
        msg.set_payload(f'<html><body>{message}</body></html>') 
        server = smtplib.SMTP_SSL(smtp_server, 465) 
        # Perform operations via server
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())  
        server.quit() 
        errorMsgIfAny = "sent"        
    except Exception as e:      
         errorMsgIfAny  =  str(e)  
    return    errorMsgIfAny 
    '''