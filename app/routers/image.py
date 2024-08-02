from typing import Annotated

from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..library.image import image

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

@router.get("/image", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse('image.html', context={'request': request})


@router.post("/image", response_class=HTMLResponse)
def summarise_post(
    request: Request,
    query: Annotated[str, Form()],
):
    result = image(query)

    return templates.TemplateResponse('image.html', context={'request': request, 'result': result})
