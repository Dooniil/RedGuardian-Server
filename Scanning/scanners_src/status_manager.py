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
                    await conn_sender.send_msg(type_msg=Message.PING)
                    name = await conn_sender.read_msg()

                    for scanner in self.all_scanner:
                        if scanner.get('name') == name:
                            self.scanner_active_connections[scanner.get('id')] = (scanner.get('address'), scanner.get('port'))

            except Exception:
                self.scanner_active_connections.pop(id)

        try:
            self.scanner_active_connections.clear()
            if self.all_scanner:
                async with asyncio.TaskGroup() as tg:
                    tasks = [tg.create_task(ping(scanner.get('address'), scanner.get('port'), scanner.get('id')))
                             for scanner in self.all_scanner]
        except Exception as e:
            pass


status_manager = StatusManager()
