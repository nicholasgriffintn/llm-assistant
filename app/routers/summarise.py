from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..library.summarise import summarise

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

@router.get("/summarise", response_class=HTMLResponse)
def form_get(request: Request):
    result = "Please enter your query"
    return templates.TemplateResponse('summarise.html', context={'request': request, 'result': result})


@router.post("/summarise", response_class=HTMLResponse)
def summarise_post(request: Request, query = Form(...)):
    result = summarise(query)

    return templates.TemplateResponse('summarise.html', context={'request': request, 'result': result})
