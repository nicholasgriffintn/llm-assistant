from typing import Annotated

from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..library.summarise import summarise

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

@router.get("/summarise", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse('summarise.html', context={'request': request})


@router.post("/summarise", response_class=HTMLResponse)
def summarise_post(
    request: Request,
    query: Annotated[str, Form()],
    should_chunk: Annotated[bool, Form()] = False,
    compare: Annotated[bool, Form()] = False
):
    result = summarise(query, should_chunk, compare)

    return templates.TemplateResponse('summarise.html', context={'request': request, 'result': result})
