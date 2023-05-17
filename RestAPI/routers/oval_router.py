from fastapi import APIRouter
from Scanning.src.upload_oval_to_db import upload_ovals


def_router = APIRouter(prefix='/definition', tags=['Definition'])


@def_router.get('/oval')
async def scan_definition():
    try:
        await upload_ovals()
        return {'status': 0}
    except Exception as e:
        return {'status': 1, 'message': str(e)}