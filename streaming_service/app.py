from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
import mysql.connector
import requests

app = FastAPI()

# MySQL connection function
def get_db():
    return mysql.connector.connect(
        host="mysql",
        user="user",
        password="password",
        database="video_db"
    )

@app.get("/videos", response_class=HTMLResponse)
def videos():
    # Fetch video list from MySQL
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT filename FROM videos")
    video_list = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    if not video_list:
        return "<h3>No videos uploaded yet.</h3>"

    # Generate links to play each video
    html_videos = "<ul>" + "".join(
        [f"<li><a href='/stream_page/{v}'>{v}</a></li>" for v in video_list]
    ) + "</ul>"

    return f"<h2>Available Videos</h2>{html_videos}"

@app.get("/stream_page/{video_name}", response_class=HTMLResponse)
def stream_page(video_name: str):
    # Ask filesystem_service whether the file exists
    response = requests.get(f"http://filesystem_service:8004/files/{video_name}")
    result = response.json()
    if "error" in result:
        raise HTTPException(status_code=404, detail="Video not found")

    html_content = f"""
    <h2>Playing: {video_name}</h2>
    <video width="720" height="480" controls>
      <source src="/stream/{video_name}" type="video/mp4">
      Your browser does not support the video tag.
    </video>
    <br><a href="/videos">Back to list</a>
    """
    return HTMLResponse(html_content)

@app.get("/stream/{video_name}")
def stream_video(video_name: str):
    # Ask filesystem_service for the file path
    response = requests.get(f"http://filesystem_service:8004/files/{video_name}")
    result = response.json()
    if "error" in result:
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(result["path"], media_type="video/mp4", filename=video_name)
