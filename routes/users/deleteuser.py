from fastapi import APIRouter  
router = APIRouter() 
@router.delete("/delete/")
async def do(): 
    return  "Delete User!"
