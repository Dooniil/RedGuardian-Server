from typing import Optional

from fastapi import APIRouter
from RestAPI.src.handlers.scanners_handler import get_scanners, remove_scanner, conn_scanner

scanner_connection_router = APIRouter(prefix='/scanners', tags=['Scanners'])


@scanner_connection_router.get('/')
async def get_active_scanners():
    return await get_scanners()


@scanner_connection_router.delete('/')
async def remove_active_scanner(scanner_name: str):
    return await remove_scanner(scanner_name)


@scanner_connection_router.post('/')
async def add_active_scanner(name: str, address: str, port: Optional[int] = 8084):
    return await conn_scanner(name, address, port)

# @credential_router.get('/')
# async def get_credential(
#         name: Optional[str] = None,
#         platform_type: PlatformOptional = 'Any',
#         created_at: Optional[str] = None,
#         updated_at: Optional[str] = None
#         ):
#     response = await CredentialHandler.get_credential_filter(
#         name=name,
#         platform_type=platform_type,
#         created_date=created_at,
#         updated_date=updated_at
#     )
#     return response
#
#
# @credential_router.get('/{credential_id}')
# async def get_credential_by_id(credential_id: int):
#     response = await CredentialHandler.get_credential(credential_id)
#     return response
#
#
# @credential_router.put('/{credential_id}')
# async def post_credential(credential_id: int, new_data: CredentialModelOptional):
#     response = await CredentialHandler.update_credential(credential_id, new_data)
#     return response
#
#
# @credential_router.delete('/{credential_id}')
# async def delete_credential_by_id(credential_id: int):
#     response = await CredentialHandler.delete_credential(credential_id)
#     return response
