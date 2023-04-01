from fastapi import APIRouter
from RestAPI.src.handlers.scanner_handler import ScannerHandler
from RestAPI.models.ScannerModel import ScannerModel


scanner_router = APIRouter(prefix='/scanners', tags=['Scanners'])


# # Add existed scanner to DB
# @scanner_router.post('/all')
# async def create_scanner(scanner_data: ScannerModel):
#     return await ScannerHandler.create_scanner(scanner_data)


# Delete existed scanner to DB
@scanner_router.delete('/all')
async def delete_scanner(scanner_id: int):
    return await ScannerHandler.delete_scanner(scanner_id)


# Get all scanner (with active, in work and non-active)
@scanner_router.get('/all')
async def get_all_scanner():
    return await ScannerHandler.get_all_scanners()


# Get only active (turn on) scanner
@scanner_router.get('/active')
async def get_active_scanners():
    return await ScannerHandler.get_active_scanners()


@scanner_router.delete('/active')
async def disconnect_from_scanner(scanner_id: int):
    return await ScannerHandler.disconnect_scanner(scanner_id)


@scanner_router.post('/in_use')
async def specify_in_use(scanner_id: int):
    return await ScannerHandler.specify_scanner(scanner_id)


@scanner_router.delete('/in_use')
async def unspecify_in_use(scanner_id: int):
    return await ScannerHandler.unspecify_scanner(scanner_id)


# broadcast searching turn on scanners
@scanner_router.get('/search')
async def broadcast(port: int = 8084, net: str = '192.168.0.0/24'):
    return await ScannerHandler.find_scanners(port, net)
