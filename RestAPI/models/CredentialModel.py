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
    login: str
    password: bytes


class CredentialModelOptional(BaseModel):
    name: Optional[str] = None
    login: Optional[str] = None
    password: Optional[bytes] = None


