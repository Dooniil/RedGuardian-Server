from fastapi import APIRouter
from RestAPI.models.HostModel import HostModel
from RestAPI.src.handlers.host_handler import HostHandler

host_router = APIRouter(prefix='/hosts', tags=['Hosts'])


@host_router.post('/')
async def create_host(host_info: HostModel):
    instance = await HostHandler.create_host(host_info)
    return instance