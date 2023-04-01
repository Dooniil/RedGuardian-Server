from typing import Optional

from pydantic import BaseModel


class CredentialModel(BaseModel):
    name: str
    login: str
    password: bytes


class CredentialModelOptional(BaseModel):
    name: Optional[str] = None
    login: Optional[str] = None
    password: Optional[bytes] = None


