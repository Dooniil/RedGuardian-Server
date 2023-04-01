from RestAPI.src.handlers.scanner_handler import ScannerHandler
from Scanning.scanners_src.status_manager import status_manager
from db.entities.Scanner import Scanner


async def get_list_in_use():
    status_manager.in_use.extend([scanner._data[0].repr for scanner in await Scanner.get_in_use()])


async def get_list_scanners():
    await get_list_in_use()
    await ScannerHandler.fetch_changes_scanners()
