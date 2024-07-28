from typing import NoReturn
from fastapi import Request, WebSocket, APIRouter
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from ..library.question import question

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

@router.get("/chatbot", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse('chatbot.html', context={'request': request})

@router.get("/chatbot/send")
async def chatbot(request: Request):
    query = request.query_params.get("query")

    return StreamingResponse(content=question(query, should_stream=True), media_type="text/event-stream")
