from fastapi import APIRouter
from models.Task import Task
from controllers import api_controller


api_router = APIRouter(prefix='/api')


@api_router.post('/tasks')
async def create_task(task: Task):
    api_controller.send_data(task)
    return {'status': 'OK'}
