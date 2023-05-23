from fastapi import APIRouter
from RestAPI.models.HostModel import HostModel
from RestAPI.src.handlers.host_handler import HostHandler


host_router = APIRouter(prefix='/hosts', tags=['Hosts'])


@host_router.post('/')
async def create_host(host_info: HostModel):
    result = await HostHandler.create_host(host_info)
    return result

@host_router.get('/{id}')
async def get_host(id: int):
    instance = await HostHandler.get_host(id)
    return instance

@host_router.put('/{id}')
async def update_host(id: int, host_info: HostModel):
    result = await HostHandler.update_host(id, host_info)
    return result

@host_router.delete('/{id}')
async def delete_host(id: int):
    result = await HostHandler.delete_host(id)
    return result