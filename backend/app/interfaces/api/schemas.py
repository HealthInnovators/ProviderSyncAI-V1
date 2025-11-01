from pydantic import BaseModel
from typing import Optional, List


class ProviderSearchRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    organization_name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    taxonomy: Optional[str] = None
    limit: int = 10


class ProviderDTO(BaseModel):
    npi: str
    enumeration_type: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    organization_name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    taxonomy: Optional[str] = None
    website: Optional[str] = None
    confidence: float


class ProviderSearchResponse(BaseModel):
    providers: List[ProviderDTO]


