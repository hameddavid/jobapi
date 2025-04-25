import httpx
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional 

# Pydantic model (as defined above)
class StudentProfile(BaseModel):
    surname: str
    firstname: str
    othernames: str
    sex: str
    program: str
    program_code: str
    dpt: str
    college: str
    college_id: str
    level: int
    email: str
    email_alternate: str
    isFresher: str
    accom_paid: float
    accom_payable: float
    special_accom_paid: Optional[float]  # -1 indicates no special accommodation
    special_accom_payable: float
    accountBalance: float
    exemption_id: Optional[int]
    exemption_reason: str

def get_student_profile(matric_number: str) -> StudentProfile:
    try: 
        url = f"https://reg.run.edu.ng/apis/profile/getstudent?matric={matric_number}"  # Replace with actual API URL
        # Using httpx to make the synchronous GET request to the remote API
        with httpx.Client() as client:
            response = client.get(url) 
        # If the response is not successful, raise an error
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch student profile")     
        # Parse and return the JSON data using Pydantic model validation
        return StudentProfile.parse_obj(response.json())
    except Exception as e:
        raise e 