import asyncio
import uvicorn
from db.database import async_db_session
from Scanning.scanners_src.conn_manager import connection_manager
from Scanning.src.server import run_server
from fastapi import FastAPI
from RestAPI.routers.credential_router import credential_router
from RestAPI.routers.encryption_router import encryption_router


app = FastAPI(title='RedGuardian REST API')
app.include_router(credential_router)
app.include_router(encryption_router)


async def async_main() -> None:
    await async_db_session.init()
    config = uvicorn.Config("main:app", port=8083, log_level="info")
    server = uvicorn.Server(config)
    periodic_checking_task = asyncio.create_task(connection_manager.periodic_check_conn())
    scanners_manager_task = asyncio.create_task(run_server(8082))
    await asyncio.gather(server.serve(), scanners_manager_task, periodic_checking_task)


if __name__ == '__main__':
    asyncio.run(async_main())
