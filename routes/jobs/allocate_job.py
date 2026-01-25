from fastapi import Depends
from sqlalchemy.orm import Session 
from utils.jobs.joballocation import   allocate_job, deallocate_job,accept_job_offer
from models.database import  get_db
from schemas.jobs.jobAllocationSchema import JobAllocation
from schemas.users.user import User
from utils.general.authentication import  user_required_roles
from .router import router   
@router.post("/allocateJob/", include_in_schema=True, response_model="")          
async def do(app_id: int, db: Session = Depends(get_db),
              TheUser: User = Depends(user_required_roles(["student","staff"]))):
   return allocate_job(app_id,TheUser, db)


@router.post("/deallocateJob/", include_in_schema=True, response_model="")          
async def do(app_id: int, db: Session = Depends(get_db),
              TheUser: User = Depends(user_required_roles(["student","staff","admin"]))):
   return deallocate_job(app_id,TheUser, db)


@router.post("/acceptJobOffer/", include_in_schema=True, response_model="")          
async def do(app_id: int, db: Session = Depends(get_db),
              TheUser: User = Depends(user_required_roles(["student","staff"]))):
   return accept_job_offer(app_id,TheUser, db)