from typing import Optional
from smolagents import Tool
from ...infrastructure.nppes import client as nppes_client


class NppesTool(Tool):
    name = "nppes_search"
    description = "Search NPPES for providers by name/location/specialty"
    inputs = {
        "first_name": str,
        "last_name": str,
        "organization_name": str,
        "city": str,
        "state": str,
        "postal_code": str,
        "taxonomy": str,
        "limit": int,
    }
    output_type = "json"

    async def __call__(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        organization_name: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        postal_code: Optional[str] = None,
        taxonomy: Optional[str] = None,
        limit: int = 10,
    ):
        return await nppes_client.search(
            first_name=first_name,
            last_name=last_name,
            organization_name=organization_name,
            city=city,
            state=state,
            postal_code=postal_code,
            taxonomy=taxonomy,
            limit=limit,
        )


