import asyncio
import json

from Scanning.scanners_src.status_manager import status_manager
from RestAPI.src.handlers.task_handler import TaskHandler
from RestAPI.src.handlers.scanner_handler import ScannerHandler
from RestAPI.src.handlers.credential_handler import CredentialHandler
from ssl_manager import ssl_manager

from pydantic import BaseModel


class TaskExecutionHandler:
    @staticmethod
    async def run_task(id: int):

        task_dict = await TaskHandler.get_task_id(id)
        custom_setting_dict = task_dict.get('custom_settings')
        scanner_dict = await ScannerHandler.get_scanner_id(task_dict.get('scanner_id'))

        if scanner_dict.get('id') not in status_manager.scanner_active_connections:
            raise Exception('Scanner isn\'t active')
        if not scanner_dict.get('in_use'):
            raise Exception('Scanner isn\'t in use')


        cred_dict = None
        if task_dict.get('credential_id'):
            cred_dict = await CredentialHandler.get_credential(task_dict.get('credential_id'))

        # task_type = task_dict.get('task')
        try:
            host = scanner_dict.get('address')
            port = scanner_dict.get('port')
            r, w = await asyncio.open_connection(host, port, ssl=ssl_manager.context)
            request = {
                'type': 'run',
                'task_data': {
                    'task_id': task_dict.get('id'),
                    'type_task': 0,
                    'settings': custom_setting_dict,
                    'credential': cred_dict,
                }
            }
            w.write(json.dumps(request).encode())
            await w.drain()
            response = await r.read(1536)
            if response != b'1':
                raise Exception('Task haven\'t sent')
            w.close()
            await w.wait_closed()
        except:
            pass
