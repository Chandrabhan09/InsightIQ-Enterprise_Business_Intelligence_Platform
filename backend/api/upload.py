from fastapi import APIRouter, UploadFile, File, HTTPException
from services.file_service import FileService
from services.logger_service import logger
import time

router = APIRouter(prefix="/api", tags=["File Upload"])

# Maximum upload size (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024

# Allowed file extensions
ALLOWED_EXTENSIONS = (".csv", ".xlsx")


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Upload a CSV or Excel dataset,
    validate it, save it,
    extract metadata,
    and log the upload.
    """

    start_time = time.time()

    # Validate filename
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is missing.")

    # Validate file extension
    if not file.filename.lower().endswith(ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400, detail="Only CSV and Excel (.xlsx) files are allowed."
        )

    # Read uploaded file
    contents = await file.read()

    # Check empty file
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # Validate file size
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 10 MB.")

    # Reset file pointer
    file.file.seek(0)

    try:
        # Save file and extract metadata
        result = FileService.save_file(file)

        processing_time = round(time.time() - start_time, 2)

        logger.info(
            f"Upload Successful | "
            f"File={file.filename} | "
            f"Time={processing_time} sec"
        )

        return {
            "success": True,
            "message": "Dataset uploaded successfully.",
            "data": result,
        }

    except Exception as e:

        logger.error(f"Upload Failed | " f"File={file.filename} | " f"Error={str(e)}")

        raise HTTPException(status_code=500, detail=str(e))
