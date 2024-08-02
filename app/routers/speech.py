from typing import Annotated

from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..library.speech import speech

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

@router.get("/speech", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse('speech.html', context={'request': request})


@router.post("/speech", response_class=HTMLResponse)
def summarise_post(
    request: Request,
    query: Annotated[str, Form()],
):
    result = speech(query)

    return templates.TemplateResponse('speech.html', context={'request': request, 'result': result, 'query': query})
