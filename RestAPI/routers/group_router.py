from fastapi import APIRouter
from RestAPI.models.HostModel import GroupModel
from RestAPI.src.handlers.group_handler import GroupHandler

group_router = APIRouter(prefix='/groups', tags=['Groups'])


@group_router.post('/')
async def create_group(group_info: GroupModel):
    instance = await GroupHandler.create_group(group_info)
    return instance

@group_router.get('/{id}')
async def get_group(id: int):
    instance = await GroupHandler.get_group(id)
    return instance

@group_router.put('/{id}')
async def update_group(id: int, group_info: GroupModel):
    instance = await GroupHandler.update_group(id, group_info)
    return instance