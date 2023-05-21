from fastapi import APIRouter
from Scanning.src.upload_oval_to_db import upload_ovals
from Scanning.src.gen_scripts import generate_execute_definition


def_router = APIRouter(prefix='/definition', tags=['Definition'])


@def_router.get('/oval')
async def scan_definition():
    try:
        await upload_ovals()
        return {'status': 0}
    except Exception as e:
        return {'status': 1, 'message': str(e)}
    
@def_router.get('/exec_definitions')
async def get_exec_definition():
    try:
        count = await generate_execute_definition()
        return {'status': 'Done', 'count': count}
    except Exception as e:
        return {'status': 1, 'message': str(e)}