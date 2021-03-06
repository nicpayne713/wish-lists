from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.library import openfile

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/about", response_class=HTMLResponse)
def about(request: Request):
    data = openfile("about.md")
    return templates.TemplateResponse("page.html", {"request": request, "data": data})
