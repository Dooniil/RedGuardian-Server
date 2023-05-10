from fastapi import APIRouter
from RestAPI.src.handlers.scanner_handler import ScannerHandler
from RestAPI.models.ScannerModel import ScannerDiscovery


scanner_router = APIRouter(prefix='/scanners', tags=['Scanners'])


# Delete existed scanner to DB
@scanner_router.delete('/{id}')
async def delete_scanner(id: int):
    return await ScannerHandler.delete_scanner(id)


# Get all scanner (with active, in work and non-active)
@scanner_router.get('/all')
async def get_all_scanner():
    return await ScannerHandler.get_all_scanners()


# Get only active (turn on) scanner
@scanner_router.get('/active')
async def get_active_scanners():
    return await ScannerHandler.get_active_scanners()


# @scanner_router.delete('/active')
# async def disconnect_from_scanner(scanner_id: int):
#     return await ScannerHandler.disconnect_scanner(scanner_id)


@scanner_router.get('/in_use/{id}')
async def specify_in_use(id: int):
    return await ScannerHandler.specify_scanner(id)


@scanner_router.get('/not_in_use/{id}')
async def unspecify_in_use(id: int):
    return await ScannerHandler.unspecify_scanner(id)

# broadcast searching turn on scanners
@scanner_router.post('/search')
async def broadcast(data: ScannerDiscovery):
    return await ScannerHandler.find_scanners(data.dict())
