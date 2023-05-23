from RestAPI.models.TaskModel import TaskModel
from RestAPI.models.TaskHostDiscoveryModel import HostDiscoveryModel
from RestAPI.models.TaskVulnerabilityModel import TaskVulnerabilityModel
from fastapi import APIRouter
from RestAPI.src.handlers.task_handler import TaskHandler
from RestAPI.src.handlers.task_execution_handler import TaskExecutionHandler

task_router = APIRouter(prefix='/task', tags=['Task'])


@task_router.post('/host-discovery')
async def create_host_discovery(task_info: TaskModel, host_discovery_info: HostDiscoveryModel):
    return await TaskHandler.create_task_hd(task_info, host_discovery_info)

@task_router.post('/vulnerability')
async def create_vulnerability(task_info: TaskModel, vulnerability_info: TaskVulnerabilityModel):
    return await TaskHandler.create_task_vuln(task_info, vulnerability_info)

# @task_router.post('/patch')
# async def create_host_discovery(task_info: TaskModel, host_discovery_info: HostDiscoveryModel):
#     return await TaskHandler.create_task_hd(task_info, host_discovery_info)


@task_router.get('/{id}')
async def get_task(id: int):
    return await TaskHandler.get_task_id(id)


@task_router.get('/run/{id}')
async def run_task(id: int):
    return await TaskExecutionHandler.run_task(id)
