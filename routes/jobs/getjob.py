from fastapi import APIRouter  
import sys
router = APIRouter() 
@router.get("/getjobs")
async def do(): 
    return {"List all jobs"}
