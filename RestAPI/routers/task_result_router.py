from fastapi import APIRouter
from RestAPI.src.handlers.task_result_handler import TaskResultHandler

task_result_router = APIRouter(prefix='/task_result', tags=['Результаты заданий '])


@task_result_router.get('/{id}', description='Запрос вернет информацию о результате сканирования')
async def get_result_task(id: int):
    return await TaskResultHandler.get_task_result(id)
