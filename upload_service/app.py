# upload_service/app.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import requests
import mysql.connector

app = FastAPI()

# MySQL connection function
def get_db():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="rootpassword",
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
    contents = await file.read()

    # Delegate file saving to filesystem_service
    response = requests.post(
        "http://filesystem_service:8004/upload",
        files={"file": (file.filename, contents, file.content_type)}
    )
    result = response.json()
    if "error" in result:
        return f"<h3>Upload failed: {result['error']}</h3>"

    filepath = result["path"]

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
