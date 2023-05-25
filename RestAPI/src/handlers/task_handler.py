import json
from RestAPI.src.handlers.credential_handler import CredentialHandler
from RestAPI.src.handlers.vulnerability_handler import VulnerabilityHandler
from Scanning.scanners_src.sender_messages import SenderMsg
from Scanning.scanners_src.status_manager import status_manager
from db.entities.Task import Task
from pydantic import BaseModel
from RestAPI.models.TaskModel import TaskStatus, TaskType
from Scanning.scanners_src.request_type import RequestType


class TaskHandler:
    @staticmethod
    async def create_task_hd(task_info: BaseModel, hd_info: BaseModel):
        task_dict: dict = task_info.dict()
        hd_dict: dict = hd_info.dict()
        hd_dict.update(
            type=hd_dict.get('type').value,
            protocols=[item.value for item in hd_dict.get('protocols')]
        )
        task_dict.update(
            task_type=TaskType.HOST_DISCOVERY.value,
            status=TaskStatus.CREATED.value,
            custom_settings=hd_dict
        )
        try:
            new_task = await Task.create(**task_dict)
            await TaskHandler.send_task(new_task.repr)
            return new_task.repr
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

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
            await TaskHandler.send_task(new_task.repr)
            return new_task.repr
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

    @staticmethod
    async def send_task(task_dict: dict):
        custom_setting_dict = task_dict.get('custom_settings')
        scanner_id = task_dict.get('scanner_id')

        if scanner_id not in status_manager.scanner_active_connections.keys():
            raise Exception('Scanner isn\'t active')

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

                
        task_sender = SenderMsg(host, port)
        request = {
            'type': RequestType.SAVE_TASK.value,
            'task_data': {
                'task_id': task_dict.get('id'),
                'type_task': task_dict.get('task_type'),
                'settings': custom_setting_dict,
                'credential': cred_dict
            },
            'run_after_creation': task_dict.get('run_after_creation')
        }
        if task_type == 1:
            request['exec_defs'] = list_exec_definition

        try:
            async with task_sender:
                await task_sender.send_msg(custom_msg=request)
                response = await task_sender.read_msg()
                if response == 0:
                    task_dict['status'] = TaskStatus.SENT.value
                    await Task.update(task_dict.get('id'), task_dict)
                else:
                    raise Exception('Error sending task')
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

    @staticmethod
    async def get_task_id(id_task):
        try:
            instance = await Task.get(id_task)
            return instance.repr
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}
