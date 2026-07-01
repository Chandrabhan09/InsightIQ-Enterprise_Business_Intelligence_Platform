from fastapi import APIRouter, UploadFile, File, HTTPException
from services.file_service import FileService

router = APIRouter(
    prefix="/api",
    tags=["File Upload"]
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):

    # Check filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    # Check extension
    allowed_extensions = (".csv", ".xlsx")

    if not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel files are allowed."
        )

    # Check file size
    contents = await file.read()

    if len(contents) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 10 MB."
        )

    # Reset file pointer
    file.file.seek(0)

    result = FileService.save_file(file)

    return {
        "success": True,
        "message": "File uploaded successfully.",
        "data": result
    }