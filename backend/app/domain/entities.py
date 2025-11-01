from pydantic import BaseModel, Field
from typing import Optional, List


class SearchQuery(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    organization_name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    taxonomy: Optional[str] = None
    limit: int = Field(10, ge=1, le=50)


class Provider(BaseModel):
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
    confidence: float = 0.0


class WebResult(BaseModel):
    title: str
    url: str
    snippet: Optional[str] = None


class ProviderSearchResult(BaseModel):
    query: SearchQuery
    providers: List[Provider]


