from fastapi import APIRouter
from Scanning.src.upload_oval_to_db import upload_ovals
from Scanning.src.gen_scripts import generate_execute_definition


def_router = APIRouter(prefix='/definition', tags=['OVAL-определения'])


@def_router.post('/json_def', description='Запрос добавит OVAL-определения в JSON формате в базу данных')
async def scan_definition():
    try:
        return await upload_ovals()
    except Exception as e:
        return {'Статус': 'Ошибка', 'Сообщение': str(e)}
    
@def_router.post('/exec_definitions', description='Запрос создаст скрипты для сканирования из OVAL-определений')
async def create_execute_definition():
    try:
        count = await generate_execute_definition()
        return {'Статус': 'Завершено', 'Сообщение': f'Создано скриптов: {count}'}
    except Exception as e:
        return {'Статус': 'Ошибка', 'Сообщение': str(e)}