from RestAPI.routers.credential_router import credential_router
from RestAPI.routers.encryption_router import encryption_router
from RestAPI.routers.scanner_router import scanner_router

routers = [encryption_router, credential_router, scanner_router]
