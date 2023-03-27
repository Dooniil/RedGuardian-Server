import asyncio
import json
import os

from singleton_decorator import singleton


@singleton
class ConnectionManager:

    def __init__(self):
        self.scanner_active_connections: dict = {}
        path_private = os.sep.join([os.getcwd(), 'RestAPI', 'encry_src', 'private.pem'])

        with open(path_private, "rb") as key_file:
            self.private_key = key_file.read()

    async def check_conn(self) -> None:

        async def ping(addr, port, key: str | int) -> None:
            try:
                r, w = await asyncio.open_connection(addr, port)
                w.close()
                await w.wait_closed()
            except Exception as e:
                print(e)
                self.scanner_active_connections.pop(key)

        if self.scanner_active_connections:
            tasks_check_conn = [asyncio.create_task(ping(conn_data[0], conn_data[1], key))
                                for key, conn_data in self.scanner_active_connections.items()]

            await asyncio.wait(tasks_check_conn)

    @property
    def list(self):
        return self.scanner_active_connections

    @property
    def names_scanners(self):
        return self.scanner_active_connections.keys()

    async def add_connection(self, name_scanner: str | int, addr: str, port: int) -> bool:
        await asyncio.wait([asyncio.create_task(self.check_conn())])
        if len(self.scanner_active_connections.keys()) + 1 <= 2:
            self.scanner_active_connections[name_scanner] = (addr, port)
            return True
        else:
            print('Too much connections')
            return False

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

    async def remove_connection(self, name_scanner: str | int):
        self.scanner_active_connections.pop(name_scanner)


connection_manager: ConnectionManager = ConnectionManager()
