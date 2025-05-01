from fastapi import APIRouter  
import sys
router = APIRouter() 
@router.get("/shout/")
async def do(): 
    return {"python_version": sys.version}
