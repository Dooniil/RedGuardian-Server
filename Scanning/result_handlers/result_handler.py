import asyncio

from RestAPI.models.TaskModel import TaskType
from RestAPI.src.handlers.task_result_handler import TaskResultHandler
from Scanning.result_handlers.result_analyzer import ResultAnalyzer


class ResultHandler:

    @staticmethod
    async def analyze_result(result: dict):
        task_result_inst = await TaskResultHandler.create_task_result(result)
        try:
            task_type = result.get('type_task')
            match task_type:
                case TaskType.HOST_DISCOVERY.value:
                    print(task_result_inst.id)
                    task_scan_results = asyncio.create_task(
                        ResultAnalyzer.host_discovery_result_analyze(task_result_inst.id, result.get('result_info'))
                    )
                    await task_scan_results
        except Exception as e:
            print(e)
