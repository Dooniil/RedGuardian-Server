from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class Type(str, Enum):
    host_discovery = 'host_discovery'


class Task(BaseModel):
    id: int
    type: Type
    network_hd: str | None
    hosts: list[int]
    scanner_id: int
    creation_date: datetime
    update_date: datetime | None

