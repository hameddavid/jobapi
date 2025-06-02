from .router import router
import sys

@router.get("/shout/")
async def do(): 
    return {"python_version": sys.version}
