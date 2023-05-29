from typing import Optional

from RestAPI.src.handlers.credential_handler import CredentialHandler
from RestAPI.models.CredentialModel import CredentialModel, CredentialModelOptional, Platform, PlatformOptional

from fastapi import APIRouter

credential_router = APIRouter(prefix='/credential', tags=['Учетные записи для сканирования'])


@credential_router.post('/', description='Запрос создаст учетную запись для сканирования.')
async def create_credential(cred_type: Platform, credential: CredentialModel):
    response = await CredentialHandler.create_new_credential(cred_type, credential)
    return response


@credential_router.get('/', description='Запрос вернет список учетных записей RedGuardian, использующихся для сканирования.')
async def get_credentials(
        name: Optional[str] = None,
        platform_type: PlatformOptional = 'Any',
        ):
    response = await CredentialHandler.get_credential_filter(
        name=name,
        platform_type=platform_type,
    )
    return response


@credential_router.get('/{id}', description='Запрос вернет данные учетной записи с указанным id.')
async def get_credential_by_id(id: int):
    response = await CredentialHandler.get_credential(id)
    return response


@credential_router.put('/{id}', description='Запрос изменит данные уже имеющейся учетной записи для сканирования с указанным id. Указывать можно только те параметры, которые требуют изменения.')
async def update_credential(id: int, new_data: CredentialModelOptional):
    response = await CredentialHandler.update_credential(id, new_data)
    return response


@credential_router.delete('/{id}', description='Запрос удалит учетную запись с указанным id.')
async def delete_credential_by_id(id: int):
    response = await CredentialHandler.delete_credential(id)
    return response
