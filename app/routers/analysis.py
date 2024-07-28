from typing import Annotated

from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..library.analysis import analysis

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

@router.get("/analysis", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse('analysis.html', context={'request': request})


@router.post("/analysis", response_class=HTMLResponse)
def summarise_post(
    request: Request,
    query: Annotated[str, Form()],
):
    result = analysis(query)

    return templates.TemplateResponse('analysis.html', context={'request': request, 'result': result})
