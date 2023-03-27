from Scanning.scanners_src.conn_manager import connection_manager


async def get_scanners() -> dict.items:
    await connection_manager.check_conn()
    return connection_manager.scanner_active_connections.items()


async def remove_scanner(scanner_name: str) -> dict:
    if connection_manager.scanner_active_connections.get(scanner_name):
        await connection_manager.remove_connection(scanner_name)
        return {'status': 'Done'}
    else:
        return {'status': 'Error', 'error_msg': 'There\'s no one scanner with such a name'}


async def conn_scanner(name: str, addr: str, port: int) -> dict:
    try:
        if await connection_manager.add_connection(name, addr, port):
            await connection_manager.send_key(addr, port)
            return {'status': 'Done'}
        return {'status': 'Undone'}
    except Exception as e:
        return {'status': 'Error', 'error_msg': e}
