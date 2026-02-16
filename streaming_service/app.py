from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
import mysql.connector
import os

app = FastAPI()

# MySQL connection function
def get_db():
    return mysql.connector.connect(
        host="mysql",
        user="user",
        password="password",
        database="video_db"
    )

VIDEO_STORAGE_PATH = "/video_storage"  # folder where upload_service saves videos

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
    file_path = os.path.join(VIDEO_STORAGE_PATH, video_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video not found")

    # HTML page with video player
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
    file_path = os.path.join(VIDEO_STORAGE_PATH, video_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(file_path, media_type="video/mp4", filename=video_name)
