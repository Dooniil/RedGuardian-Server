from fastapi import APIRouter
from RestAPI.src.handlers.task_result_handler import TaskResultHandler

task_result_router = APIRouter(prefix='/task_result', tags=['Task Result'])


@task_result_router.get('/{id}')
async def get_task(id: int):
    return await TaskResultHandler.get_task_result(id)
