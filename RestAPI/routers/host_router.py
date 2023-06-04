from fastapi import APIRouter, Query
from typing import Optional
from RestAPI.models.HostModel import HostModel, HostModelHD
from RestAPI.src.handlers.host_handler import HostHandler


host_router = APIRouter(prefix='/hosts', tags=['Хосты'])


@host_router.post('/', description='Запрос для добавления хостов в базу данных')
async def create_host(host_info: HostModel):
    result = await HostHandler.create_host(host_info)
    return result

@host_router.post('/hd', description='Запрос для добавления хостов в базу данных из результата сканирования ')
async def create_host_by_host_discovery_result(
    task_result_id: int, 
    groups: Optional[list[int]] = Query(None, description='Определяет группы, в которые добавятся хосты')
    ):
    result = await HostHandler.create_host_by_hd(task_result_id, groups)
    return result

@host_router.get('/{id}', description='Запрос вернет информацию о хосте')
async def get_host(id: int):
    instance = await HostHandler.get_host(id)
    return instance

@host_router.put('/{id}', description='Запрос для изменения данных уже существующего хоста')
async def update_host(id: int, host_info: HostModel):
    result = await HostHandler.update_host(id, host_info)
    return result

@host_router.delete('/{id}', description='Запрос на удаление хоста')
async def delete_host(id: int):
    result = await HostHandler.delete_host(id)
    return result