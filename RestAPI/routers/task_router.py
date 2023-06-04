from RestAPI.models.TaskModel import TaskModel
from RestAPI.models.TaskHostDiscoveryModel import HostDiscoveryModel, TypeHD, TypeProtocol
from RestAPI.models.TaskVulnerabilityModel import TaskVulnerabilityModel
from fastapi import APIRouter, Query
from RestAPI.src.handlers.task_handler import TaskHandler
from RestAPI.src.handlers.task_execution_handler import TaskExecutionHandler

task_router = APIRouter(prefix='/task', tags=['Задания'])


@task_router.post('/host-discovery', description='Запрос создаст задание типа Обнаружение хостов')
async def create_host_discovery(
    task_info: TaskModel, 
    subnets: list[str] = Query('192.168.50.0/24', description='Подсеть для поиска хостов'), 
    type_scan: TypeHD = Query(TypeHD.Only_host_scan, description='Определяет, какие данные попадут в результат задания'),
    protocols: list[TypeProtocol] = Query(TypeProtocol.TCP, description='Протокол для поиска хостов'),
    ):
    host_discovery_info = dict(
        subnets=subnets,
        type=type_scan,
        protocols=protocols,
    )
    return await TaskHandler.create_task_hd(task_info, host_discovery_info)

@task_router.post('/vulnerability', description='Запрос создаст задание типа Аудит уязвимостей')
async def create_vulnerability(task_info: TaskModel, vulnerability_info: TaskVulnerabilityModel):
    return await TaskHandler.create_task_vuln(task_info, vulnerability_info)

# @task_router.post('/patch')
# async def create_host_discovery(task_info: TaskModel, host_discovery_info: HostDiscoveryModel):
#     return await TaskHandler.create_task_hd(task_info, host_discovery_info)


@task_router.get('/{id}', description='Запрос вернет информацию о задании')
async def get_task(id: int):
    return await TaskHandler.get_task_id(id)


@task_router.get('/send/{id}', description='Запрос отправит задание службе сканирования для записи в файл, если в момент создания задания модуль Worker был неактивен')
async def send_task(id: int):
    return await TaskHandler.send_task_by_id(id)


@task_router.get('/run/{id}', description='Запрос запустит выполнение задания, записанного в модуле Worker')
async def run_task(id: int):
    return await TaskExecutionHandler.run_task(id)
