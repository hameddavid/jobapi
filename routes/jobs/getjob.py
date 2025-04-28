from fastapi import APIRouter  
import sys
router = APIRouter() 
@router.get("/getjobs")
async def list_job_url_func(): 
    return {"List all jobs"}
