import json
import asyncio

from Scanning.result_handlers.result_handler import ResultHandler
from Scanning.scanners_src.ssl_manager import ssl_manager
from Scanning.scanners_src.request_type import RequestType


async def read_request(reader) -> str:
    request = bytearray()
    while True:
        request += await reader.read(1536)
        reader.feed_eof()
        if reader.at_eof():
            return request.decode()


async def controller_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    request = await read_request(reader)
    #  TODO send response

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
                print(result_dict)
                task_result = asyncio.create_task(ResultHandler.analyze_result(result_dict))
                await task_result
    except json.decoder.JSONDecodeError:
        pass


async def run_server(host: str, port: int) -> None:
    server = await asyncio.start_server(controller_handler, host, port, ssl=ssl_manager.context)
    async with server:
        await server.serve_forever()
