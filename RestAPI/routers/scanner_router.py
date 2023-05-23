from fastapi import APIRouter
from RestAPI.src.handlers.scanner_handler import ScannerHandler
from RestAPI.models.ScannerModel import ScannerDiscovery


scanner_router = APIRouter(prefix='/scanners', tags=['Scanners'])


@scanner_router.post('/search')
async def broadcast(data: ScannerDiscovery):
    return await ScannerHandler.find_scanners(data.dict())

@scanner_router.get('/all')
async def get_all_scanner():
    return await ScannerHandler.get_all_scanners()

@scanner_router.get('/update_all')
async def update_list_scanners():
    await ScannerHandler.check_scanners_activity()
    await ScannerHandler.fetch_changes_active()
    return {'status': 0}

@scanner_router.get('/in_use/{id}')
async def specify_in_use(id: int):
    return await ScannerHandler.specify_scanner(id)


@scanner_router.get('/not_in_use/{id}')
async def unspecify_in_use(id: int):
    return await ScannerHandler.unspecify_scanner(id)

@scanner_router.delete('/{id}')
async def delete_scanner(id: int):
    return await ScannerHandler.delete_scanner(id)