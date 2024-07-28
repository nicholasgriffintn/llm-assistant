from typing import Annotated

from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..library.question import question

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

@router.get("/question", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse('question.html', context={'request': request})


@router.post("/question", response_class=HTMLResponse)
def summarise_post(
    request: Request,
    query: Annotated[str, Form()],
):
    result = question(query)

    return templates.TemplateResponse('question.html', context={'request': request, 'result': result})
