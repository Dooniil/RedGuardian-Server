from fastapi import APIRouter, Query
from RestAPI.src.handlers.scanner_handler import ScannerHandler


scanner_router = APIRouter(prefix='/scanners', tags=['Службы сканирования (RedGuardian Worker)'])


@scanner_router.post('/search', description='Поиск служб сканирования в указанной подсети. Продолжительность поиска: примерно 10-15 секунд.')
async def broadcast(subnet: str = Query('192.168.50.0/24', description='Подсеть в формате 0.0.0.0/24'),
    port: int = Query(8084, description='Порт, на котором работает служба сканирования')):
    data = dict(subnet=subnet, port=port)
    return await ScannerHandler.find_scanners(data)

@scanner_router.get('/all', description='Запрос вернет список всех служб сканирования, находящихся в БД.')
async def get_all_scanner():
    return await ScannerHandler.get_all_scanners()

@scanner_router.get('/{id}', description='Запрос вернет данные службы сканирования с указанным id.')
async def get_scanner_by_id(id: int):
    return await ScannerHandler.get_scanner_id(id)

@scanner_router.get('/update', description='Запрос вернет список активных служб сканирования.')
async def update_list_active_scanners():
    await ScannerHandler.check_scanners_activity()
    active_scanner: list = await ScannerHandler.fetch_changes_active()
    return {
        'Статус': 'Завершено', 
        'Сообщение': f'Обнаружено активных сканеров: {len(active_scanner)}',
        'ID активных сканнеров': active_scanner}

@scanner_router.put('/in_use/{id}', description='Запрос сделает службу сканирования доступной для работы')
async def specify_in_use(id: int):
    return await ScannerHandler.specify_scanner(id)


@scanner_router.put('/not_in_use/{id}', description='Запрос сделает службу сканирования не доступной для работы')
async def unspecify_in_use(id: int):
    return await ScannerHandler.unspecify_scanner(id)

@scanner_router.delete('/{id}', description='Запрос удалит службу сканирования из БД.')
async def delete_scanner(id: int):
    return await ScannerHandler.delete_scanner(id)