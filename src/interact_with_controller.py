import asyncio
import json


async def get_response_from_controller() -> bytes:
    reader, writer = await asyncio.open_connection('127.0.0.1', 8082)

    request = dict()
    request['from'] = 'rest'

    writer.write(json.dumps(request, indent=1).encode('utf-8'))
    await writer.drain()

    while True:
        try:
            response = await reader.read(1536)

            if response:
                return response
            elif not response:
                print('Controller connection is failed')
                break

        finally:
            writer.close()
            await writer.wait_closed()
