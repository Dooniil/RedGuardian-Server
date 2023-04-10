from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
import os

from RestAPI.routers.scanner_router import get_all_scanner

pages_router = APIRouter(tags=['Pages'])

templates = Jinja2Templates(directory=os.sep.join([os.getcwd(), 'Frontend', 'templates']))


@pages_router.get('/')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@pages_router.get('/scanners')
def get_base_page(request: Request, scanners=Depends(get_all_scanner)):
    return templates.TemplateResponse('scanners.html', {'request': request, 'scanners': scanners})
