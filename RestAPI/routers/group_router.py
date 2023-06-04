from fastapi import APIRouter
from RestAPI.models.HostModel import GroupModel
from RestAPI.src.handlers.group_handler import GroupHandler

group_router = APIRouter(prefix='/groups', tags=['Группы хостов'])


@group_router.post('/', description='Запрос для создания группы')
async def create_group(group_info: GroupModel):
    result = await GroupHandler.create_group(group_info)
    return result

@group_router.get('/{id}', description='Запрос вернет информацию о группе')
async def get_group(id: int):
    instance = await GroupHandler.get_group(id)
    return instance

@group_router.put('/{id}', description='Запрос для изменения данных группы')
async def update_group(id: int, group_info: GroupModel):
    result = await GroupHandler.update_group(id, group_info)
    return result

@group_router.delete('/{id}', description='Запрос для удаления группы')
async def delete_group(id: int):
    result = await GroupHandler.delete_group(id)
    return result