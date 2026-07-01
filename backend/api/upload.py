from fastapi import APIRouter, UploadFile, File, HTTPException
from services.file_service import FileService

router = APIRouter(
    prefix="/api",
    tags=["File Upload"]
)

# Maximum upload size (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Allowed file extensions
ALLOWED_EXTENSIONS = (".csv", ".xlsx")


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):

    # Check if filename exists
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    # Validate extension
    if not file.filename.lower().endswith(ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel (.xlsx) files are allowed."
        )

    # Read file into memory
    contents = await file.read()

    # Check if file is empty
    if len(contents) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # Validate file size
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 10 MB."
        )

    # Reset file pointer
    file.file.seek(0)

    # Save file
    result = FileService.save_file(file)

    return {
        "success": True,
        "message": "Dataset uploaded successfully.",
        "data": result
    }