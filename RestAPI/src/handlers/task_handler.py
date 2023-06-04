import json
from RestAPI.src.handlers.credential_handler import CredentialHandler
from RestAPI.src.handlers.vulnerability_handler import VulnerabilityHandler
from Scanning.scanners_src.sender_messages import SenderMsg
from Scanning.scanners_src.status_manager import status_manager
from db.entities.Task import Task
from pydantic import BaseModel
from RestAPI.models.TaskModel import TaskStatus, TaskType
from Scanning.scanners_src.request_type import RequestType
from db.entities.Host import Host


type_hd = {
    'Только поиск хостов': 0,
    'Определение ОС': 1,
    'Сканирование общих портов': 2,
    'Сканирование всех портов': 3,
    'Другое': 4
}


type_protocol = {
    'TCP': 0,
    'ICMP': 1,
    'UDP': 2
}


class TaskHandler:
    @staticmethod
    async def create_task_hd(task_info: BaseModel, host_discovery_dict: dict):
        task_dict: dict = task_info.dict()
        host_discovery_dict.update(
            type=type_hd.get((host_discovery_dict.get('type')).value),
            protocols=[type_protocol.get(item.value) for item in host_discovery_dict.get('protocols')]
        )
        task_dict.update(
            task_type=TaskType.HOST_DISCOVERY.value,
            status=TaskStatus.CREATED.value,
            custom_settings=host_discovery_dict
        )
        try:
            new_task = await Task.create(**task_dict)
            response = await TaskHandler.send_task(new_task.repr)
            return {'Статус': 'Завершено', 'ID Задания': new_task.id, 'Сообщение': response.get('Сообщение')}
        except Exception as e:
            return {'Cтатус': 'Ошибка', 'Сообщение': e}

    @staticmethod
    async def create_task_vuln(task_info: BaseModel, vuln_info: BaseModel):
        task_dict: dict = task_info.dict()
        vuln_dict: dict = vuln_info.dict()
        
        task_dict.update(
            task_type=TaskType.VULNERABILITY.value,
            status=TaskStatus.CREATED.value,
            custom_settings=vuln_dict
        )
        try:
            new_task = await Task.create(**task_dict)
            response = await TaskHandler.send_task(new_task.repr)
            return {'Статус': 'Завершено', 'ID Задания': new_task.id, 'Сообщение': response.get('Сообщение')}
        except Exception as e:
            return {'Cтатус': 'Ошибка', 'Сообщение': e}

    @staticmethod
    async def send_task(task_dict: dict):
        custom_setting_dict = task_dict.get('custom_settings')
        scanner_id = task_dict.get('scanner_id')

        if scanner_id not in status_manager.scanner_active_connections.keys():
            raise Exception('Служба сканирования не активна')

        host, port = status_manager.scanner_active_connections.get(scanner_id)

        cred_dict = None
        if task_dict.get('credential_id'):
            cred_dict = await CredentialHandler.get_credential(task_dict.get('credential_id'))
            cred_dict.update(login=cred_dict.get('login').decode(), password=cred_dict.get('password').decode())
            cred_dict.pop('created_at')
            cred_dict.pop('updated_at')

        task_type = task_dict.get('task_type')
        match task_type:
            case 1:
                family = cred_dict.get('family')
                list_exec_definition = await VulnerabilityHandler.get_exec_definition(family)
                hosts = list()
                for id in custom_setting_dict.get('hosts_id'):
                    host_instance = await Host.get(id)
                    hosts.append(dict(id=id, ip=host_instance.ip, dns=host_instance.dns, family=host_instance.family, cpe=host_instance.cpe))
                
        task_sender = SenderMsg(host, port)
        request = {
            'type': RequestType.SAVE_TASK.value,
            'task_data': {
                'task_id': task_dict.get('id'),
                'type_task': task_dict.get('task_type'),
                'credential': cred_dict
            },
            'run_after_creation': task_dict.get('run_after_creation')
        }
        if task_type == 0:
            request['task_data']['settings'] = task_dict.get('custom_settings')
        elif task_type == 1:
            request['task_data']['exec_defs'] = list_exec_definition
            request['task_data']['settings'] = dict(hosts=hosts)

        try:
            async with task_sender:
                await task_sender.send_msg(custom_msg=request)
                response = int(await task_sender.read_msg())
                if response == 0:
                    task_dict['status'] = TaskStatus.SENT.value
                    await Task.update(task_dict.get('id'), task_dict)
                    return {'Статус': 'Завершено', 'Сообщение': 'Задание отправлено'}
                else:
                    raise Exception('Ошибка во время отправки задания')
        except Exception as e:
            return {'Cтатус': 'Ошибка', 'Сообщение': e}

    @staticmethod
    async def send_task_by_id(id):
        task_dict = (await Task.get(id)).repr
        custom_setting_dict = task_dict.get('custom_settings')
        scanner_id = task_dict.get('scanner_id')

        if scanner_id not in status_manager.scanner_active_connections.keys():
            raise Exception('Служба сканирования не активна')

        host, port = status_manager.scanner_active_connections.get(scanner_id)

        cred_dict = None
        if task_dict.get('credential_id'):
            cred_dict = await CredentialHandler.get_credential(task_dict.get('credential_id'))
            cred_dict.update(login=cred_dict.get('login').decode(), password=cred_dict.get('password').decode())
            cred_dict.pop('created_at')
            cred_dict.pop('updated_at')

        task_type = task_dict.get('task_type')
        match task_type:
            case 1:
                family = cred_dict.get('family')
                list_exec_definition = await VulnerabilityHandler.get_exec_definition(family)
                hosts = list()
                for id in custom_setting_dict.get('hosts_id'):
                    host_instance = await Host.get(id)
                    hosts.append(dict(id=id, ip=host_instance.ip, dns=host_instance.dns, family=host_instance.family, cpe=host_instance.cpe))
                
        task_sender = SenderMsg(host, port)
        request = {
            'type': RequestType.SAVE_TASK.value,
            'task_data': {
                'task_id': task_dict.get('id'),
                'type_task': task_dict.get('task_type'),
                'credential': cred_dict
            },
            'run_after_creation': task_dict.get('run_after_creation')
        }
        if task_type == 0:
            request['task_data']['settings'] = task_dict.get('custom_settings')
        elif task_type == 1:
            request['task_data']['exec_defs'] = list_exec_definition
            request['task_data']['settings'] = dict(hosts=hosts)

        try:
            async with task_sender:
                await task_sender.send_msg(custom_msg=request)
                response = int(await task_sender.read_msg())
                if response == 0:
                    task_dict['status'] = TaskStatus.SENT.value
                    await Task.update(task_dict.get('id'), task_dict)
                    return {'Статус': 'Завершено', 'Сообщение': 'Задание отправлено'}
                else:
                    raise Exception('Ошибка во время отправки задания')
        except Exception as e:
            return {'Cтатус': 'Ошибка', 'Сообщение': e}


    @staticmethod
    async def get_task_id(id_task):
        try:
            instance = await Task.get(id_task)
            return instance.repr
        except Exception as e:
            return {'Cтатус': 'Ошибка', 'Сообщение': e}