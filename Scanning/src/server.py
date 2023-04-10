import json
import asyncio
from ssl_manager import ssl_manager
from Scanning.scanners_src.status_manager import status_manager


async def controller_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    addr, port = writer.get_extra_info('peername')
    msg = await reader.read(1536)
    data = json.loads(msg)

    # type_req = data.get('cmd')
    # name = data.get('name_scanner')
    # match type_req:
    #     case 'connecting':
    #         await connection_manager.add_connection(name, addr, port)
    #         await connection_manager.send_key(addr, port)
        # case 'request':
        #     pass
        # case 'closing':
        #     connection_manager.remove_connection(name)


async def run_server(host: str, port: int) -> None:
    server = await asyncio.start_server(controller_handler, host, port, ssl=ssl_manager.context)
    async with server:
        await server.serve_forever()
