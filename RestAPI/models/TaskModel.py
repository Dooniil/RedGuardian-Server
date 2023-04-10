from pydantic import BaseModel
from enum import Enum


class TaskType(Enum):
    HOST_DISCOVERY = 0


class TaskModel(BaseModel):
    name: str
    description: str | None
    credential_id: int | None
    scanner_id: int
    run_after_creation: bool = False


