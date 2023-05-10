import asyncio
from pathlib import Path

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from db.database import async_db_session
from Scanning.src.server import run_server
from fastapi import FastAPI
from RestAPI.routers.list_routers import routers
from RestAPI.src.start_loading import start_funcs
from Frontend.pages.pages_router import pages_router
# from address import choose_host

app = FastAPI(title='RedGuardian REST API')
for router in routers:
    app.include_router(router, prefix='/api')

app.include_router(pages_router)

app.mount(
    "/Frontend/style",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "RedGuardian-Server/Frontend/style"),
    name="style",
)
app.mount(
    "/Frontend/scripts",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "RedGuardian-Server/Frontend/scripts"),
    name="scripts",
)

origins = [
    # "http://10.0.0.183:8083",
    "http://192.168.50.223:8083",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def startup():
    await start_funcs()


# connecting to DB, start REST API and Controller
async def async_main() -> None:
    # host = choose_host()
    # host = '10.0.0.183'
    host = '192.168.50.223'
    await async_db_session.init()
    await async_db_session.check_connection()

    config = uvicorn.Config("main:app", port=8083, host=host, log_level="info")
    server = uvicorn.Server(config)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(run_server(host, 8082)),
        tg.create_task(server.serve())


if __name__ == '__main__':
    asyncio.run(async_main())
