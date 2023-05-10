from typing import Optional
from pydantic import BaseModel


class ScannerModel(BaseModel):
    name: str
    address: str = '192.168.0.0'
    port: Optional[int] = 8084
    description: Optional[str] = ''


class ScannerDiscovery(BaseModel):
    subnet: str
    port: Optional[int] = 8084
