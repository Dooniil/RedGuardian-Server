from RestAPI.src.handlers.task_result_handler import TaskResultHandler
from Scanning.scanners_src.sender_messages import SenderMsg
from Scanning.scanners_src.status_manager import status_manager
from RestAPI.src.handlers.task_handler import TaskHandler
from Scanning.scanners_src.request_type import RequestType


class TaskExecutionHandler:
    @staticmethod
    async def run_task(id: int):
        task_dict = await TaskHandler.get_task_id(id)
        scanner_id = task_dict.get('scanner_id')

        if scanner_id not in status_manager.scanner_active_connections:
            raise Exception('Scanner isn\'t active')

        host, port = status_manager.scanner_active_connections[scanner_id]

        try:
            run_sender = SenderMsg(host, port)
            request = {
                'type': RequestType.RUN_TASK.value,
                'task_id': id
            }
            async with run_sender:
                await run_sender.send_msg(custom_msg=request)

            # await TaskResultHandler.create_task_result(id)
        except Exception as e:
            pass


