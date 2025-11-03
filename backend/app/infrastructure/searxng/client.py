from typing import Any, Dict, List, Optional
from urllib.parse import urljoin
import httpx
from ..settings import settings
from ..http import get
from ..logging import get_logger


logger = get_logger(__name__)


async def search(query: str, *, categories: Optional[str] = None, num_results: int = 10) -> List[dict]:
    """
    Search using SearXNG. Returns empty list on failure to gracefully handle rate limits.
    """
    try:
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
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 429:
            logger.warning("searxng_rate_limited", query=query[:50], message="Rate limited by SearXNG, skipping web enrichment")
        else:
            logger.warning("searxng_http_error", query=query[:50], status_code=e.response.status_code, message=str(e))
        return []
    except Exception as e:
        logger.warning("searxng_search_failed", query=query[:50], error=str(e))
        return []  # Return empty list on any error to not break the main flow


