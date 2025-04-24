from fastapi import APIRouter  
import sys
router = APIRouter() 
@router.get("/getapplications")
async def do(): 
    return {"List all applications"}
