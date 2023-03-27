import json
import asyncio
from Scanning.scanners_src.conn_manager import connection_manager


async def controller_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    addr, port = writer.get_extra_info('peername')
    msg = await reader.read(1536)
    data = json.loads(msg)

    type_req = data.get('cmd')
    name = data.get('name_scanner')
    match type_req:
        case 'connecting':
            if await connection_manager.add_connection(name, addr, port):
                await connection_manager.send_key(addr, port)
        # case 'request':
        #     pass
        # case 'closing':
        #     connection_manager.remove_connection(name)


async def run_server(port: int) -> None:
    server = await asyncio.start_server(controller_handler, '10.0.0.183', port)
    async with server:
        await server.serve_forever()
