# upload_service/app.py
from fastapi import FastAPI, File, UploadFile, Request, Form, Depends
from fastapi.responses import HTMLResponse
import shutil
import mysql.connector
import os

app = FastAPI()

# Ensure video storage folder exists
os.makedirs("video_storage", exist_ok=True)

# MySQL connection function
def get_db():
    return mysql.connector.connect(
        host="mysql",      # Docker Compose service name
        user="root",
        password="rootpassword",   # match your docker-compose
        database="video_db"
    )

@app.get("/upload", response_class=HTMLResponse)
def upload_form():
    return """
    <h2>Upload Video</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        Username: <input type="text" name="username"><br>
        Select video: <input type="file" name="file"><br>
        <input type="submit" value="Upload">
    </form>
    """

@app.post("/upload", response_class=HTMLResponse)
async def upload_file(file: UploadFile = File(...), username: str = Form(...)):
    filepath = f"/video_storage/{file.filename}"
    # Save the file
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Insert metadata into MySQL
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO videos (filename, filepath, uploaded_by) VALUES (%s, %s, %s)",
        (file.filename, filepath, username)
    )
    db.commit()
    cursor.close()
    db.close()

    return f"<h3>{file.filename} uploaded successfully. <a href='http://localhost:8001/videos'>Go to Videos</a></h3>"
