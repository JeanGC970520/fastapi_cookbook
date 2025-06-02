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
    dir_path = os.path.realpath(__file__).replace("main.py", "") # Using to get root dir of main.py module
    with open(f"{dir_path}/uploads/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

@app.get(
    "/downloadfile/{filename}",
    response_class= FileResponse,
)
async def dowload_file(filename: str):
    dir_path = os.path.realpath(__file__).replace("main.py", "")
    if not Path(f"{dir_path}/uploads/{filename}").exists():
        raise HTTPException(
            status_code=404,
            detail=f"file {filename} not found",
        )
    return FileResponse(
        path=f"{dir_path}/uploads/{filename}", filename=filename,
    )

