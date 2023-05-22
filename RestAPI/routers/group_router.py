from fastapi import APIRouter
from RestAPI.models.HostModel import GroupModel
from RestAPI.src.handlers.group_handler import GroupHandler

group_router = APIRouter(prefix='/groups', tags=['Groups'])


@group_router.post('/')
async def create_group(group_info: GroupModel):
    instance = await GroupHandler.create_host(group_info)
    return instance