from typing import Optional

from pydantic import BaseModel
from enum import Enum


class Platform(str, Enum):
    Linux = 'Linux',
    Windows = 'Windows',


class PlatformOptional(str, Enum):
    Any = 'Any'
    Linux = 'Linux',
    Windows = 'Windows',


class CredentialModel(BaseModel):
    name: str
    login: bytes
    password: bytes
    family: int


class CredentialModelOptional(BaseModel):
    name: Optional[str] = None
    login: Optional[bytes] = None
    password: Optional[bytes] = None
    family: Optional[int] = None


