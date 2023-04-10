from db.entities.Task import Task
from pydantic import BaseModel


class TaskHandler:
    @staticmethod
    async def create_task_hd(task_info: BaseModel, hd_info: BaseModel):
        task_dict = task_info.dict()
        task_dict['task_type'] = 0
        hd_dict = hd_info.dict()
        hd_dict.update(
            type=hd_dict.get('type').value,
            protocols=[item.value for item in hd_dict.get('protocols')]
        )
        task_dict.update(custom_settings=hd_dict)
        try:
            new_task = await Task.create(**task_dict)
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

        return new_task.repr

    @staticmethod
    async def get_task_id(id_task):
        try:
            instance = (await Task.get(id_task))[0]
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

        return instance.repr
