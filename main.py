import uvicorn
from fastapi import FastAPI
from routers import api_router
from sender import Sender


if __name__ == '__main__':
    app = FastAPI(title='RedGuardian REST API')
    app.include_router(api_router)

    @app.on_event('startup')
    def startup():
        sender = Sender()
        sender.connect_to_controller('127.0.0.1', 8999)

    uvicorn.run(app, port=8000, host='127.0.0.1')

