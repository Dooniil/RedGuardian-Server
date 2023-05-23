from typing import Optional

from RestAPI.src.handlers.credential_handler import CredentialHandler
from RestAPI.models.CredentialModel import CredentialModel, CredentialModelOptional, Platform, PlatformOptional

from fastapi import APIRouter

credential_router = APIRouter(prefix='/credential', tags=['Credentials'])


@credential_router.post('/')
async def post_credential(cred_type: Platform, credential: CredentialModel):
    response = await CredentialHandler.create_new_credential(cred_type, credential)
    return response


@credential_router.get('/')
async def get_credential(
        name: Optional[str] = None,
        platform_type: PlatformOptional = 'Any',
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
        ):
    response = await CredentialHandler.get_credential_filter(
        name=name,
        platform_type=platform_type,
        created_date=created_at,
        updated_date=updated_at
    )
    return response


@credential_router.get('/{id}')
async def get_credential_by_id(id: int):
    response = await CredentialHandler.get_credential(id)
    return response


@credential_router.put('/{id}')
async def post_credential(id: int, new_data: CredentialModelOptional):
    response = await CredentialHandler.update_credential(id, new_data)
    return response


@credential_router.delete('/{id}')
async def delete_credential_by_id(id: int):
    response = await CredentialHandler.delete_credential(id)
    return response
