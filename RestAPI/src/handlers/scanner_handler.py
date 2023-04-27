import asyncio
import ipaddress
from Scanning.scanners_src.status_manager import status_manager
from db.entities.Scanner import Scanner
from RestAPI.src.encryption import EncyptionManager
from Scanning.scanners_src.sender_messages import SenderMsg, Message


class ScannerHandler:
    @staticmethod
    async def delete_scanner(scanner_id):
        try:
            await Scanner.delete(scanner_id)
            status_manager.scanner_active_connections.pop(scanner_id)
            status_manager.all_scanner.pop(scanner_id)
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

        return {'status': 'Done'}

    @staticmethod
    async def get_all_scanners():
        return status_manager.all_scanner

    @staticmethod
    async def get_scanner_id(id_scanner):
        try:
            instance = await Scanner.get(id_scanner)
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

        return instance.repr

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
            status_manager.scanner_active_connections.pop(scanner_id)
            for scanner in status_manager.all_scanner:
                if scanner.get('id') == scanner_id:
                    scanner.pop('active')
            return {'status': 'Done'}
        except Exception:
            return {'status': 'Error', 'error_msg': 'There\'s no one scanner with such a name'}

    @staticmethod
    async def specify_scanner(scanner_id: int):
        if scanner_id in status_manager.scanner_active_connections:
            scanner_dict: dict = await ScannerHandler.get_scanner_id(scanner_id)
            try:
                scanner_dict.update(in_use=True)
                await Scanner.update(scanner_id, scanner_dict)
                await EncyptionManager.send_key(scanner_dict.get('address'), scanner_dict.get('port'))
            except Exception as e:
                return {'status': 'Error', 'error_msg': e}
            status_manager.in_use.append(scanner_id)
            return {'status': 'Done'}
        return {'status': 'Undone', 'msg': 'Scanner isn\'t active'}

    @staticmethod
    async def unspecify_scanner(scanner_id: int):
        if scanner_id in status_manager.scanner_active_connections:
            scanner_dict: dict = await ScannerHandler.get_scanner_id(scanner_id)
            try:
                scanner_dict.update(in_use=False)
                await Scanner.update(scanner_id, scanner_dict)
                status_manager.in_use.remove(scanner_id)
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
                ping_sender = SenderMsg(str(host), port)
                async with ping_sender:
                    await ping_sender.send_msg(type_msg=Message.PING)
                    name = await ping_sender.read_msg()

                is_new_scanners, id = await check_in_db(name, str(host))
                status_manager.scanner_active_connections[id] = (str(host), port)
            except Exception as e:
                pass

        try:
            network = ipaddress.ip_network(broadcast)
            async with asyncio.TaskGroup() as ping_tg:
                tasks = [ping_tg.create_task(ping(str(host))) for host in network.hosts()]

            if is_new_scanners:
                await ScannerHandler.fetch_changes_scanners()

            await ScannerHandler.fetch_changes_active()
            return {'status': 'Done'}

        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

