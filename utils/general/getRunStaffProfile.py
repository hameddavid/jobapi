import httpx
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional 

# Pydantic model (as defined above)
class StaffProfile(BaseModel):
    status: str
    title: str
    userid: str
    firstname: str
    middlename: str
    lastname: str
    staff_no: str
    institution: str
    faculty: str
    dept: str
    programme: str
    staff_level: str
    level_step: str
    staff_type: str  


   

def get_staff_profile(emailAddy: str) -> StaffProfile:
    try:
        url = f"https://staff.run.edu.ng/getStaff.php?email={emailAddy}&staff_profile=staff_profile"  # Replace with actual API URL
        # Using httpx to make the synchronous GET request to the remote API
        with httpx.Client(verify = False) as client:
            response = client.get(url) 
        # If the response is not successful, raise an error
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch staff profile (code={response.status_code})")     
        # Parse and return the JSON data using Pydantic model validation
        return StaffProfile.parse_obj(response.json())
    except Exception as e:
        raise e