from fastapi import   HTTPException,status
from sqlalchemy.orm import Session
from schemas.users.user import User
from schemas.apps.appschema import CreateAppSchema
from models.applications import applications as appModel
from models.jobs import jobs as jobModel
import os
import uuid
import aiofiles # For async file operations
from sqlalchemy import select


# --- Configuration for file storage ---
# IMPORTANT: Adjust this path for your production environment!
UPLOAD_DIRECTORY = "uploads/applications"
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


async def create_app(appData: CreateAppSchema, ThisUser:User, db: Session ):  

        # check if the job is still available
        # job = db.query(jobModel).filter(jobModel.id == appData.job_id).first()
        # if not job or job.deleted == 'Y' or job.status != 'OPEN':
        #     raise HTTPException(status_code=404, detail="Job not available.")
    stored_filepath_for_cleanup = None
    
    try:
        # 1. Validate Job Existence
        job = db.execute(select(jobModel).where(jobModel.id == appData.job_id)).scalar_one_or_none()
        if not job or job.deleted == 'Y' or job.status.value != 'OPEN':
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job with ID {appData.job_id} not available."
            )
        
         # 2. Check if user has already applied for this job
        existing_application = db.execute(
            select(appModel)
            .where(appModel.user_id == ThisUser.id, appModel.job_id == appData.job_id)
        ).scalar_one_or_none()
        if existing_application:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already applied for this job."
            )
            
        db_application = appModel(
            title = appData.title,
            narration = appData.narration,
            suitable_price = appData.suitable_price,
            user_id = ThisUser.id,
            job_id = appData.job_id  # Placeholder for document path, will be set after file processing
            
          
        )
        db.add(db_application)
        db.flush() # IMPORTANT: This assigns ID to db_application, needed for ApplicationDocument FK

        # 4. Process and store documents
        if appData.doc_1:
            doc_file = appData.doc_1
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
            unique_filename = f"{db_application.id}_{uuid.uuid4()}{file_extension}"
            stored_filepath = os.path.join(UPLOAD_DIRECTORY, unique_filename)
            stored_filepath_for_cleanup = stored_filepath
            # Save the file asynchronously to disk
            async with aiofiles.open(stored_filepath, "wb") as buffer:
                await buffer.write(file_content)
            
            # Create ApplicationDocument record (in session, but not committed)
            db_application.doc_1 = stored_filepath
        
        # 5. Commit the entire transaction (Application and all ApplicationDocuments)
        db.commit()
        db.refresh(db_application) # Refresh to get latest state including auto-generated IDs and loaded relationships
        return db_application # FastAPI/Pydantic will serialize this ORM object

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
    



    
    
    
    
    
