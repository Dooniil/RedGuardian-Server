from fastapi import APIRouter
from RestAPI.models.HostModel import GroupModel
from RestAPI.src.handlers.group_handler import GroupHandler

group_router = APIRouter(prefix='/groups', tags=['Groups'])


@group_router.post('/')
async def create_group(group_info: GroupModel):
    result = await GroupHandler.create_group(group_info)
    return result

@group_router.get('/{id}')
async def get_group(id: int):
    instance = await GroupHandler.get_group(id)
    return instance

@group_router.put('/{id}')
async def update_group(id: int, group_info: GroupModel):
    result = await GroupHandler.update_group(id, group_info)
    return result

@group_router.delete('/{id}')
async def delete_group(id: int):
    result = await GroupHandler.delete_group(id)
    return result