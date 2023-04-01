import asyncio
import ipaddress

from Scanning.scanners_src.status_manager import status_manager
from db.entities.Scanner import Scanner


class ScannerHandler:
    @staticmethod
    async def delete_scanner(scanner_id):
        try:
            await Scanner.delete(scanner_id)
            status_manager.scanner_active_connections.pop(scanner_id)
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

        return {'status': 'Done'}

    @staticmethod
    async def get_all_scanners():
        return status_manager.all_scanner

    @staticmethod
    async def fetch_changes_scanners():
        status_manager.all_scanner.clear()
        try:
            status_manager.all_scanner.extend([scanner._data[0].repr for scanner in await Scanner.get_all()])
        except Exception as e:
            pass

    @staticmethod
    async def fetch_changes_active():
        for scanner in status_manager.all_scanner:
            if scanner.get('id') in status_manager.scanner_active_connections:
                scanner['active'] = True

    @staticmethod
    async def get_active_scanners() -> dict.items:
        await status_manager.check_conn()  # update list of active scanners
        return status_manager.scanner_active_connections

    @staticmethod
    async def disconnect_scanner(scanner_id: int) -> dict:
        try:
            await status_manager.disconnect_connection(scanner_id)
            return {'status': 'Done'}
        except Exception:
            return {'status': 'Error', 'error_msg': 'There\'s no one scanner with such a name'}

    @staticmethod
    async def specify_scanner(scanner_id: int):
        if scanner_id in status_manager.scanner_active_connections:
            for scanner in status_manager.all_scanner:
                if scanner.get('id') == scanner_id:
                    try:
                        scanner['in_use'] = True
                        await Scanner.update(scanner_id, scanner)
                    except Exception as e:
                        return {'status': 'Error', 'error_msg': e}
                    status_manager.in_use.append(scanner)
                    return {'status': 'Done'}
        return {'status': 'Undone', 'msg': 'Scanner isn\'t active'}

    @staticmethod
    async def unspecify_scanner(scanner_id: int):
        for i, scanner in enumerate(status_manager.in_use):
            if scanner.get('id') == scanner_id:
                try:
                    scanner['in_use'] = False
                    await Scanner.update(scanner_id, scanner)
                    status_manager.in_use.pop(i)
                    return {'status': 'Done'}
                except Exception as e:
                    return {'status': 'Error', 'error_msg': e}
        return {'status': 'Undone', 'msg': 'Scanner isn\'t in use'}

    @staticmethod
    async def find_scanners(port: int, broadcast: str):
        is_new_scanners = False

        async def check_in_db(name, addr):
            instance = await Scanner.get_by_name(name)
            if not instance:
                instance = await Scanner.create(name=name, address=addr, port=port)
                return True, instance.id
            return False, instance._data[0].id

        async def ping(host: str):
            nonlocal is_new_scanners
            try:
                r, w = await asyncio.open_connection(str(host), port)
                w.write(b'p')  # p = ping
                await w.drain()
                name = (await r.read(1536)).decode()
                w.close()
                await w.wait_closed()
                is_new_scanners, id_ = await check_in_db(name, str(host))
                await status_manager.add_active_connection(id_, str(host), port)
            except Exception:
                pass

        try:
            network = ipaddress.ip_network(broadcast)
            tasks = [asyncio.create_task(ping(str(host))) for host in network.hosts()]
            await asyncio.wait(tasks)

            if is_new_scanners:
                await ScannerHandler.fetch_changes_scanners()

            await ScannerHandler.fetch_changes_active()
            return {'status': 'Done'}

        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

