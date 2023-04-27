import asyncio
import json
from enum import Enum

from Scanning.scanners_src.ssl_manager import ssl_manager


class Message(str, Enum):
    PING = 'p'
    CONNECTION = 'c'


class SenderMsg:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.reader: asyncio.StreamReader | None = None
        self.writer: asyncio.StreamWriter | None = None

    async def send_msg(self, custom_msg: dict = None, type_msg: Message = None):
        msg: bytes = bytes()
        if custom_msg:
            msg: bytes = json.dumps(custom_msg).encode()
        if type_msg:
            msg: bytes = type_msg.value.encode()

        self.writer.write(msg)
        await self.writer.drain()

    async def read_msg(self):
        msg = (await self.reader.read(1536)).decode()
        return msg

    async def __aenter__(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port, ssl=ssl_manager.context)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.writer.close()
        await self.writer.wait_closed()
        if exc_val:
            raise

