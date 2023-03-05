import uvicorn
from fastapi import FastAPI
from routers import api_router


if __name__ == '__main__':
    app = FastAPI(title='RedGuardian REST API')
    app.include_router(api_router)

    @app.on_event('startup')
    def startup():
        pass
    uvicorn.run(app, port=8083, host='127.0.0.1')

