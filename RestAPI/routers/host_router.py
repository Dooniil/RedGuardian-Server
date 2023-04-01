from fastapi import APIRouter

host_router = APIRouter(prefix='/hosts', tags=['Encryption'])


@host_router.post('/')
async def create_host():

    return