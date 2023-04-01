import asyncio


class StatusManager:

    def __init__(self):
        self.scanner_active_connections: dict[int, tuple] = {}
        self.all_scanner: list = []
        self.in_use: list = []

    # checking state of connected scanners
    async def check_conn(self) -> None:
        async def ping(addr, port, id_) -> None:
            try:
                r, w = await asyncio.open_connection(addr, port)
                w.write(b'c')
                await w.drain()
                w.close()
                await w.wait_closed()
            except asyncio.TimeoutError:
                self.scanner_active_connections.pop(id_)

        if self.scanner_active_connections:
            tasks_check_conn = [asyncio.create_task(ping(conn_data[0], conn_data[1], scanner_id))
                                for scanner_id, conn_data in self.scanner_active_connections.items()]
            await asyncio.wait(tasks_check_conn)


status_manager: StatusManager = StatusManager()
