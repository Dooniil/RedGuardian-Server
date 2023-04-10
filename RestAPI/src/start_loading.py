from RestAPI.src.handlers.scanner_handler import ScannerHandler
from Scanning.scanners_src.status_manager import status_manager
import asyncio
from RestAPI.src.encryption import EncyptionManager


async def get_list_in_use():
    for scanner in status_manager.all_scanner:
        if scanner.get('in_use'):
            status_manager.in_use.append(scanner)
            if scanner.get('active'):
                await EncyptionManager.send_key(scanner.get('address'), scanner.get('port'))


async def get_list_scanners():
    await ScannerHandler.fetch_changes_scanners()


async def read_keys():
    await asyncio.wait([
        asyncio.create_task(EncyptionManager.get_private_key()),
        asyncio.create_task(EncyptionManager.get_public_key())
    ])


async def broadcast(subnet: str):
    await ScannerHandler.find_scanners(8084, subnet)


async def start_funcs():
    tasks = [
        asyncio.create_task(get_list_scanners()),
        asyncio.create_task(read_keys()),
        asyncio.create_task(broadcast('192.168.50.0/24'))
    ]
    await asyncio.wait(tasks)
    await get_list_in_use()
