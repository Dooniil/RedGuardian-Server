import asyncio
from Scanning.scanners_src.sender_messages import SenderMsg, Message


class StatusManager:
    def __init__(self):
        self.scanner_active_connections: dict[int, tuple] = {}
        self.all_scanner: list[dict] = []
        self.in_use: list[int] = []

    # checking state of connected scanners
    async def check_conn(self) -> None:
        async def ping(host, port, id) -> None:
            try:
                conn_sender = SenderMsg(host, port)
                async with conn_sender:
                    await conn_sender.send_msg(type_msg=Message.CONNECTION)
            except asyncio.TimeoutError:
                self.scanner_active_connections.pop(id)

        if self.scanner_active_connections:
            async with asyncio.TaskGroup() as tg:
                tasks = [tg.create_task(ping(conn_data[0], conn_data[1], scanner_id))
                         for scanner_id, conn_data in self.scanner_active_connections.items()]


status_manager: StatusManager = StatusManager()
