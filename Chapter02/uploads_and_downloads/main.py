import os
import shutil
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

# Base application
app = FastAPI()


@app.post("/uploadfile")
async def upload_file(
    file: UploadFile = File(...),  # Suspensive dots -> Field(...) meaning that is required
):
    """ Endpoint to upload a file into the server
    Args:
        file: required file to save it
    Headers:
        Content-Type: must be equal to multipart/form-data
    """
    dir_path = os.path.realpath(__file__).replace("main.py", "") # Using to get root dir of main.py module
    with open(f"{dir_path}/uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

@app.get(
    "/downloadfile/{filename}",
    response_class= FileResponse,
)
async def dowload_file(filename: str):
    """ Endpoint to download file, FastAPI has a FileResponse to help us
    with this task. It streams files from the server
    Args:
        filename: name of file to get its content
    """
    dir_path = os.path.realpath(__file__).replace("main.py", "")
    if not Path(f"{dir_path}/uploads/{filename}").exists():
        raise HTTPException(
            status_code=404,
            detail=f"file {filename} not found",
        )
    return FileResponse(
        path=f"{dir_path}/uploads/{filename}", filename=filename,
    )

