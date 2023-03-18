import asyncio
import json
import os

from cryptography.hazmat.primitives import serialization
from singleton_decorator import singleton


@singleton
class ConnectionManager:

    def __init__(self):
        self.scanner_active_connections: dict = {}
        path_private = os.sep.join([os.getcwd(), 'RestAPI', 'encry_src', 'private.pem'])

        with open(path_private, "rb") as key_file:
            self.private_key = key_file.read()

    async def __check_conn(self, conn_data: dict, key: str | int) -> None:
        try:
            r, w = await asyncio.open_connection(conn_data[0], conn_data[1])
            w.close()
            await w.wait_closed()
        except Exception as e:
            print(e)
            self.scanner_active_connections.pop(key)

    async def periodic_check_conn(self):
        while True:
            print(self.scanner_active_connections)
            if self.scanner_active_connections:
                tasks_check_conn = [asyncio.create_task(self.__check_conn(conn_data, key))
                                    for key, conn_data in self.scanner_active_connections.items()]

                _, _ = await asyncio.wait(tasks_check_conn)
            await asyncio.sleep(10)

    @property
    def list(self):
        return self.scanner_active_connections

    @property
    def names_scanners(self):
        return self.scanner_active_connections.keys()

    async def add_connection(self, name_scanner: str | int, conn_info: tuple):
        self.scanner_active_connections[name_scanner] = conn_info
        await self.send_key(conn_info)

    async def send_key(self, conn_data: tuple) -> None:
        try:
            r, w = await asyncio.open_connection(conn_data[0], conn_data[1])

            w.write(self.private_key)
            await w.drain()
            response = await r.read(1536)

            if response != b'1':
                raise Exception('The key didn\'t send')

            w.close()
            await w.wait_closed()

        except Exception as e:
            print(e)

    def remove_connection(self, name_scanner: str | int):
        self.scanner_active_connections.pop(name_scanner)


connection_manager: ConnectionManager = ConnectionManager()
