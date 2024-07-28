from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from .library.helpers import *
from app.routers import summarise, analysis, question, chatbot

load_dotenv()

app = FastAPI()


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(summarise.router)
app.include_router(analysis.router)
app.include_router(question.router)
app.include_router(chatbot.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = openfile("home.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def show_page(request: Request, page_name: str):
    data = openfile(page_name+".md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
