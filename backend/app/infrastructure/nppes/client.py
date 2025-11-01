from typing import Any, Dict, List, Optional
from urllib.parse import urljoin
from ..settings import settings
from ..http import get


# NOTE: to avoid circular import name shadowing, we import settings via alias module below.


def _build_params(
    first_name: Optional[str],
    last_name: Optional[str],
    organization_name: Optional[str],
    city: Optional[str],
    state: Optional[str],
    postal_code: Optional[str],
    taxonomy: Optional[str],
    limit: int,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {"version": "2.1", "limit": limit}
    if first_name:
        params["first_name"] = first_name
    if last_name:
        params["last_name"] = last_name
    if organization_name:
        params["organization_name"] = organization_name
    if city:
        params["city"] = city
    if state:
        params["state"] = state
    if postal_code:
        params["postal_code"] = postal_code
    if taxonomy:
        params["taxonomy_description"] = taxonomy
    return params


async def search(
    *,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    organization_name: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    postal_code: Optional[str] = None,
    taxonomy: Optional[str] = None,
    limit: int = 10,
) -> List[dict]:
    params = _build_params(first_name, last_name, organization_name, city, state, postal_code, taxonomy, limit)
    base_url = str(settings.nppes_base_url).rstrip("/")
    url = f"{base_url}/"
    resp = await get(url, params=params)
    data = resp.json()
    return data.get("results", [])


