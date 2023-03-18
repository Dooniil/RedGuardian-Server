from RestAPI.src.handlers.credential_handler import CredentialHandler
from RestAPI.models.CredentialModel import CredentialModel, Platform

from fastapi import APIRouter

credential_router = APIRouter(prefix='/credential', tags=['Credentials'])


@credential_router.post('/')
async def post_credential(cred_type: Platform, credential: CredentialModel):
    response = await CredentialHandler.create_new_credential(cred_type, credential)
    return response
