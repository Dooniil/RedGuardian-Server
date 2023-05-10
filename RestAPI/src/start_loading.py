from RestAPI.src.handlers.scanner_handler import ScannerHandler
from Scanning.scanners_src.status_manager import status_manager
import asyncio
from RestAPI.src.encryption import EncyptionManager


async def get_list_in_use():
    for scanner in status_manager.all_scanner:
        if scanner.get('in_use'):
            status_manager.in_use.append(scanner.get('id'))
            if scanner.get('active'):
                await EncyptionManager.send_key(scanner.get('address'), scanner.get('port'))


async def get_list_scanners():
    await ScannerHandler.fetch_changes_scanners()


async def read_keys():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(EncyptionManager.get_private_key()),
        tg.create_task(EncyptionManager.get_public_key())


async def broadcast(subnet: str):
    await ScannerHandler.find_scanners({'subnet': subnet, 'port': 8084})


async def start_funcs():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(get_list_scanners()),
        tg.create_task(read_keys()),
        tg.create_task(broadcast('10.0.0.0/24'))

    await get_list_in_use()
