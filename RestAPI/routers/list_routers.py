from RestAPI.routers.credential_router import credential_router
from RestAPI.routers.encryption_router import encryption_router
from RestAPI.routers.scanner_router import scanner_router
from RestAPI.routers.task_router import task_router
from RestAPI.routers.task_result_router import task_result_router
from RestAPI.routers.oval_router import def_router 


routers = [encryption_router, credential_router, scanner_router, task_router, task_result_router, def_router]
