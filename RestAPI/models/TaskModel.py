from pydantic import BaseModel
from enum import Enum


#  This is only for info
class TaskStatus(Enum):
    CREATED = 0
    SENT = 1
    IN_PROGRESS = 2
    DONE = 3
    ERROR = 4


class TaskType(Enum):
    HOST_DISCOVERY = 0


class TaskModel(BaseModel):
    name: str
    description: str | None
    credential_id: int | None
    scanner_id: int
    run_after_creation: bool = False


