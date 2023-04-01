import asyncio
import json
from singleton_decorator import singleton
from db.entities.Scanner import Scanner
from RestAPI.src.encryption import get_private_key


@singleton
class StatusManager:

    def __init__(self):
        self.scanner_active_connections: dict[int, tuple] = {}
        self.all_scanner: list = []
        self.in_use: list = []
        self.private_key = get_private_key()

    # checking state of connected scanners
    async def check_conn(self) -> None:
        async def ping(addr, port, id_) -> None:
            try:
                r, w = await asyncio.open_connection(addr, port)
                w.write('c'.encode())
                await w.drain()
                w.close()
                await w.wait_closed()
            except asyncio.TimeoutError:
                self.scanner_active_connections.pop(id_)

        if self.scanner_active_connections:
            tasks_check_conn = [asyncio.create_task(ping(conn_data[0], conn_data[1], scanner_id))
                                for scanner_id, conn_data in self.scanner_active_connections.items()]
            await asyncio.wait(tasks_check_conn)

    async def add_active_connection(self, scanner_id: int, addr: str, port: int):
        self.scanner_active_connections[scanner_id] = (addr, port)

    # TODO replace to encryption or keys_handler
    async def send_key(self, addr: str, port: int) -> None:
        try:
            r, w = await asyncio.open_connection(addr, port)
            request = json.dumps(
                {'type': 'key', 'key': self.private_key.decode(encoding="raw_unicode_escape")}
            ).encode()
            w.write(request)
            await w.drain()

            response = await r.read(1536)

            if response != b'1':
                raise Exception('The key didn\'t send')

            w.close()
            await w.wait_closed()

        except Exception as e:
            print(e)

    # TODO add_connection
    async def disconnect_connection(self, scanner_id: int):
        self.scanner_active_connections.pop(scanner_id)


status_manager: StatusManager = StatusManager()
