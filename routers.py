import asyncio

from fastapi import APIRouter
from models.Task import Task
from src.interact_with_controller import get_response_from_controller

api_router = APIRouter(prefix='/api')


@api_router.get('/some')
async def get_some():
    task = asyncio.create_task(get_response_from_controller())
    response = await task
    return response
