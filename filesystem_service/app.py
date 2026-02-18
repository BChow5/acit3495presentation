from fastapi import FastAPI, UploadFile, File
import os
import shutil

app = FastAPI()
STORAGE_DIR = "/video_storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    path = os.path.join(STORAGE_DIR, file.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"path": path}

@app.get("/files/{filename}")
def get_file(filename: str):
    path = os.path.join(STORAGE_DIR, filename)
    if os.path.exists(path):
        return {"path": path}
    return {"error": "File not found"}
