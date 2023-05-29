import asyncio
from db.entities.Task import Task
from RestAPI.models.TaskModel import TaskType, TaskStatus
from RestAPI.src.handlers.task_result_handler import TaskResultHandler
from RestAPI.src.handlers.task_handler import TaskHandler
from Scanning.result_handlers.result_analyzer import ResultAnalyzer


class ResultHandler:

    @staticmethod
    async def analyze_result(result: dict):
        task_result_inst = await TaskResultHandler.create_task_result(result)
        try:
            task_type = result.get('type_task')
            match task_type:
                case TaskType.HOST_DISCOVERY.value:
                    task_scan_results = asyncio.create_task(
                        ResultAnalyzer.host_discovery_result_analyze(task_result_inst.id, result.get('result_info'))
                    )
                    await task_scan_results
                case TaskType.VULNERABILITY.value:
                    task_scan_results = asyncio.create_task(
                        ResultAnalyzer.vulnerability_result_analyze(task_result_inst.id, result.get('result_info'))
                    )
                    await task_scan_results
                    task_dict = await TaskHandler.get_task_id(result.get('task_id'))
                    task_dict['status'] = TaskStatus.DONE.value
                    await Task.update(task_dict.get('id'), task_dict)
        except Exception as e:
            print(e)
