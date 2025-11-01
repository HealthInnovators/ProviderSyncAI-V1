from typing import Any, Dict, List, Optional
from urllib.parse import urljoin
from ..settings import settings
from ..http import get


async def search(query: str, *, categories: Optional[str] = None, num_results: int = 10) -> List[dict]:
    base = str(settings.searxng_url)
    url = urljoin(base if base.endswith('/') else base + '/', 'search')
    params: Dict[str, Any] = {
        "q": query,
        "format": "json",
        "language": "en",
        "safesearch": 1,
    }
    if categories:
        params["categories"] = categories
    resp = await get(url, params=params)
    data = resp.json()
    results = data.get("results", [])
    return results[:num_results]


