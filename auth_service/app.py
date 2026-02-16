# auth_service/app.py
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse

app = FastAPI()

# Dummy users
users = {"brandon": "password", "carson": "password", "kurtis": "password"}

@app.get("/", response_class=HTMLResponse)
def login_page():
    return """
    <h2>Login</h2>
    <form action="/login" method="post">
        Username: <input type="text" name="username"><br>
        Password: <input type="password" name="password"><br>
        Choose page:
        <select name="destination">
            <option value="upload">Upload Video</option>
            <option value="stream">Stream Video</option>
        </select><br>
        <input type="submit" value="Login">
    </form>
    """

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), destination: str = Form(...)):
    if users.get(username) == password:
        # Redirect to chosen page
        if destination == "upload":
            return RedirectResponse(url="http://localhost:8000/upload", status_code=303)
        else:
            return RedirectResponse(url="http://localhost:8001/videos", status_code=303)
    return HTMLResponse("<h3>Login failed. <a href='/'>Try again</a></h3>")


