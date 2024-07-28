from typing import NoReturn
from fastapi import Request, WebSocket, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..library.question import question

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

@router.get("/chatbot", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse('chatbot.html', context={'request': request})

@router.websocket("/chatbot/ws")
async def websocket_endpoint(websocket: WebSocket) -> NoReturn:
    await websocket.accept()
    try:
        while True:
            text_data = await websocket.receive_text()
            query = text_data

            async for chunks in question(query, should_stream=True):
                await websocket.send_text(chunks)

    except Exception as e:
        print(f'WebSocket error: {str(e)}')
    finally:
        await websocket.close()