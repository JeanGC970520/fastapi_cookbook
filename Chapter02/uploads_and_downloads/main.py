import os
import shutil
from fastapi import FastAPI, File, UploadFile

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
