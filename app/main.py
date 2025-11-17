from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.router import api_router
import datetime

app = FastAPI(title="CuraLink API", version="0.1")
templates = Jinja2Templates(directory="app/template")

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    server_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    context = {
        "request": request,
        "status": "Online✅",
        "uptime": server_time,
        "server_name": "Curalink Backend Server",
        "version": "1.0.0"
    }
    return templates.TemplateResponse("index.html", context)
