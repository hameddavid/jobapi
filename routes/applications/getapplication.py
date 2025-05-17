from .router import router

@router.get("/getapplications")
async def do(): 
    return {"List all applications"}
