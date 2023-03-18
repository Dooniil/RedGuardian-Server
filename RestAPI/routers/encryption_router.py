from fastapi import APIRouter
from RestAPI.src.handlers.encryption_handler import gen_keys

encryption_router = APIRouter(prefix='/encryption', tags=['Encryption'])


@encryption_router.post('/', description='Generate public and private keys according a significant size')
async def create_keys(size: int):
    res_msg = gen_keys(size)
    return res_msg
