import os
from fastapi import APIRouter, HTTPException

# Initialize the router
router = APIRouter(
    prefix="/files",
    tags=["files"],
    responses={404: {"description": "Not found"}},
)

# Define the directory where files are uploaded
UPLOAD_DIRECTORY = os.path.expanduser("~/backend-MR/files")

@router.get("/")
async def list_uploaded_files():
    try:
        # Check if the directory exists
        if not os.path.exists(UPLOAD_DIRECTORY):
            raise HTTPException(status_code=404, detail="Upload directory not found")

        # List all files in the directory
        files = os.listdir(UPLOAD_DIRECTORY)

        # Filter out any directories or unwanted files if necessary
        files = [file for file in files if os.path.isfile(os.path.join(UPLOAD_DIRECTORY, file))]

        return {"uploaded_files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")
