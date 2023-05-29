from datetime import datetime
from db.entities.Task_result import TaskResult


class TaskResultHandler:
    @staticmethod
    async def create_task_result(result: dict):
        try:
            instance = await TaskResult.create(
                task_id=result.get('task_id'),
                exec_time=datetime.strptime(result.get('exec_time'), '%H:%M:%S').time(),
                start_at=datetime.strptime(result.get('start_time'), '%Y-%m-%d %H:%M:%S'),
                end_at=datetime.strptime(result.get('end_time'), '%Y-%m-%d %H:%M:%S'),
            )
            return instance
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

    @staticmethod
    async def get_task_result(id: int):
        try:
            task_result = (await TaskResult.get_relationship(id, TaskResult.scan_results)).repr

        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}
