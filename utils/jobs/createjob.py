from fastapi import   HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas.users.user import User
from schemas.jobs.job import JobCreate
from models.jobs import jobs as jobModel, jobCategory
import os
import uuid
import aiofiles # For async file operations


# --- Configuration for file storage ---
# IMPORTANT: Adjust this path for your production environment!
UPLOAD_DIRECTORY = "uploads/jobs"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True) # Create the directory if it doesn't exist

# --- Allowed file types and size limits ---
ALLOWED_FILE_TYPES = {
    "application/pdf",
    "application/msword",
    "image/jpeg",
    "image/png",
    "image/gif",
}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024 # 10 MB


async def create_job(jobData: JobCreate, ThisUser:User, db: Session ):  
    stored_filepath_for_cleanup = None  # Initialize for cleanup    
    try:
        
        # 2. Check if job category exists
        check_cat = db.execute(
            select(jobCategory)
            .where(jobCategory.id == jobData.cat_id)
        ).scalar_one_or_none()
        if not check_cat:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No such job category found. Please select a valid category."
            )
        newJob = jobModel(
            title = str(jobData.title).capitalize(),
            description =  str(jobData.description).capitalize(),
            listed_price = jobData.listed_price,
            location = jobData.location,
            keywords = jobData.keywords,
            job_category_id = jobData.cat_id,
            user_id = ThisUser.id
        )
        db.add(newJob)
        db.flush()

        if jobData.doc_1:
            doc_file = jobData.doc_1
            if doc_file.content_type not in ALLOWED_FILE_TYPES:
                raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {doc_file.content_type} for {doc_file.filename}. Allowed types are: {', '.join(ALLOWED_FILE_TYPES)}"
            )

            
            # Read file content and check size
            file_content = await doc_file.read()
            file_size = len(file_content)
            if file_size == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File {doc_file.filename} is empty."
                )
            if file_size > MAX_FILE_SIZE_BYTES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"File {doc_file.filename} is too large. Max size is {MAX_FILE_SIZE_BYTES / (1024*1024):.1f}MB."
                )

            # Generate a unique filename and path
            file_extension = os.path.splitext(doc_file.filename)[1]
            unique_filename = f"{newJob.id}_{uuid.uuid4()}{file_extension}"
            stored_filepath = os.path.join(UPLOAD_DIRECTORY, unique_filename)
            stored_filepath_for_cleanup = stored_filepath
            # Save the file asynchronously to disk
            async with aiofiles.open(stored_filepath, "wb") as buffer:
                await buffer.write(file_content)
            
            # Create ApplicationDocument record (in session, but not committed)
            newJob.doc_1 = stored_filepath
                
                # 5. Commit the entire transaction (Application and all ApplicationDocuments)
        db.commit()
        db.refresh(newJob) # Refresh to get latest state including auto-generated IDs and loaded relationships
        return newJob # FastAPI/Pydantic will serialize this ORM object

    except HTTPException as e:
        db.rollback() # Rollback DB changes
        # Clean up any files that were written before the error
        if stored_filepath_for_cleanup and os.path.exists(stored_filepath_for_cleanup):
            os.remove(stored_filepath_for_cleanup)
        raise e
    except Exception as e:
        db.rollback() # Rollback DB changes
        # Clean up any files that were written before the error
        if stored_filepath_for_cleanup and os.path.exists(stored_filepath_for_cleanup):
            os.remove(stored_filepath_for_cleanup)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {e}"
        )
    




