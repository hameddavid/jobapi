from fastapi import FastAPI
from fastapi import FastAPI, Depends
from fastapi.openapi.models import OAuthFlows, SecurityScheme
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, OAuthFlowPassword
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware


from routes.general  import   shout
from routes.users  import   createuser, signInUser, updateuser,  deleteuser
from routes.students import createstudent, getstudent, updatestudent, loginstudent
from routes.staff import createstaff, getstaff, updatestaff, loginstaff
from routes.admins import createadmin, getadmin, sendpassresetlinkadmin,updateadmin, activateadmin
from routes.admins import verifyadmin, resetpasswordadmin, loginadmin
from routes import jobs
from routes.applications import getapplication
import asyncio 
app = FastAPI(
     title="JobPosting - Redeemer's University",
     version="1.0.0",
     description="Job Posting  - Redeemer's University"
    
) 

# Define the origins that are allowed to make requests
origins = [
    "http://localhost:3039",  # Your React app's URL
    "http://127.0.0.1:3039",  # Include this if using localhost with IP
    "http://jobs.run.edu.ng",
    "http://jobs.run.edu.ng:80"

   
]

#origins = ["*"]   # used this line only during development, before we go live
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow only specified origins
    allow_credentials=True,  # Allow cookies and credentials if needed
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# app.include_router(shout.router, tags=["General"]) 

# app.include_router(createuser.router, tags=["AUTH"])
app.include_router(signInUser.router, tags=["AUTH"]) 
# app.include_router(updateuser.router, tags=["AUTH"])
# app.include_router(deleteuser.router, tags=["AUTH"])

app.include_router(getstudent.router, tags=["Students"]) 
app.include_router(createstudent.router, tags=["Students"])
app.include_router(updatestudent.router, tags=["Students"]) 
app.include_router(loginstudent.router, tags=["Students"]) 

app.include_router(getstaff.router, tags=["Staff"])
app.include_router(createstaff.router, tags=["Staff"])
app.include_router(updatestaff.router, tags=["Staff"]) 
app.include_router(loginstaff.router, tags=["Staff"]) 

app.include_router(activateadmin.router, tags=["Admins"])
app.include_router(getadmin.router, tags=["Admins"]) 
app.include_router(createadmin.router, tags=["Admins"]) 
app.include_router(loginadmin.router, tags=["Admins"])
app.include_router(resetpasswordadmin.router, tags=["Admins"])
app.include_router(updateadmin.router, tags=["Admins"])
app.include_router(sendpassresetlinkadmin.router, tags=["Admins"])
app.include_router(verifyadmin.router, tags=["Admins"]) 



 

app.include_router(jobs.router,prefix="/job", tags=["Jobs"])


app.include_router(getapplication.router, tags=["Jobs.Applications"]) 

@app.get("/", tags=["General"])
async def read_root():
    return {"Sup 1!"} 