import aiofiles
import aiofiles.os
import os
from db.entities.Definition import JsonDefinition
import json

path = os.sep.join([os.getcwd(), 'db', 'json'])


async def upload_ovals():
    for file in os.listdir(path):
        file_path = os.sep.join([path, file])
        def_dict = dict()

        async with aiofiles.open(file_path, mode='r') as write_handle:
            json_text = await write_handle.read()
            
        if 'win_def' in file:
            family = 1
        elif 'nix_def' in file:
            family = 2

        oval_dict: dict = json.loads(json_text)
        title = oval_dict['definitions'][0]['metadata']['title']
        description = oval_dict['definitions'][0]['metadata']['description']
        def_dict.update(json_format=oval_dict, family=family, title=title, description=description) 

        await JsonDefinition.create(**def_dict)
    return {'Статус': 'Завершено', 'Сообщение': f'Добавлено OVAL-определений в JSON: {len(os.listdir(path))}'}