import json
import asyncio

from Scanning.result_handlers.result_handler import ResultHandler
from Scanning.scanners_src.ssl_manager import ssl_manager
from Scanning.scanners_src.request_type import RequestType


async def readexactly(reader, bytes_count: int) -> bytes:
    """
    Функция приёма определённого количества байт
    """
    data_bytes = bytearray()
    while len(data_bytes) < bytes_count: # Пока не получили нужное количество байт
        part = await reader.read(bytes_count - len(data_bytes)) # Получаем оставшиеся байты
        if not part: # Если из сокета ничего не пришло, значит его закрыли с другой стороны
            raise IOError("Соединение потеряно")
        data_bytes += part
    return data_bytes

async def reliable_receive(reader) -> bytes:
    """
    Функция приёма данных
    Обратите внимание, что возвращает тип bytes
    """
    data_bytes = bytearray()
    while True:
        part_len = int.from_bytes(await readexactly(reader, 2), "big") # Определяем длину ожидаемого куска
        if part_len == 0: # Если пришёл кусок нулевой длины, то приём окончен
            return data_bytes
        data_bytes += await readexactly(reader, part_len) # Считываем сам кусок


async def controller_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    request = await reliable_receive(reader)
    try:
        data = json.loads(request)
        match data.get('type'):
            case RequestType.ERROR.value:
                error_dict = data.get('error_info')
                print(error_dict)
            case RequestType.RESULT.value:
                result_dict = {
                    'result_info': data.get('result_info'),
                    'task_id': data.get('task_id'),
                    'type_task': data.get('type_task'),
                    'start_time': data.get('start_time'),
                    'end_time': data.get('end_time'),
                    'exec_time': data.get('exec_time')
                }
                task_result = asyncio.create_task(ResultHandler.analyze_result(result_dict))
                await task_result
    except json.decoder.JSONDecodeError:
        pass


async def run_server(host: str, port: int) -> None:
    server = await asyncio.start_server(controller_handler, host, port, ssl=ssl_manager.context)
    async with server:
        await server.serve_forever()
