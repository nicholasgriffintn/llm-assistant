from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

@router.get("/summarise", response_class=HTMLResponse)
def form_get(request: Request):
    result = "Please enter your query"
    return templates.TemplateResponse('summarise.html', context={'request': request, 'result': result})


@router.post("/summarise", response_class=HTMLResponse)
def form_post1(request: Request, query = Form(...)):
    # TODO: Call the summarise function from the summarise module

    print(query)

    result = "Eventually, this will be the summarised text from the AI model"
    return templates.TemplateResponse('summarise.html', context={'request': request, 'result': result})
