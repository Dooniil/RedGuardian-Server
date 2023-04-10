from RestAPI.models.TaskModel import TaskModel
from RestAPI.models.TaskHostDiscoveryModel import HostDiscoveryModel
from fastapi import APIRouter
from RestAPI.src.handlers.task_handler import TaskHandler

task_router = APIRouter(prefix='/task', tags=['Task'])


@task_router.post('/host-discovery')
async def create_host_discovery(task_info: TaskModel, host_discovery_info: HostDiscoveryModel):
    return await TaskHandler.create_task_hd(task_info, host_discovery_info)


@task_router.get('/{id}')
async def get_task(id: int):
    return await TaskHandler.get_task_id(id)
#
# @task_router.get('/')
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
# @task_router.get('/{credential_id}')
# async def get_credential_by_id(credential_id: int):
#     response = await CredentialHandler.get_credential(credential_id)
#     return response
#
#
# @task_router.put('/{credential_id}')
# async def post_credential(credential_id: int, new_data: CredentialModelOptional):
#     response = await CredentialHandler.update_credential(credential_id, new_data)
#     return response
#
#
# @task_router.delete('/{credential_id}')
# async def delete_credential_by_id(credential_id: int):
#     response = await CredentialHandler.delete_credential(credential_id)
#     return response
