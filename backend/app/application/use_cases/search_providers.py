import hashlib
import json
from typing import List
from ...domain.entities import SearchQuery, Provider, ProviderSearchResult
from ...infrastructure.nppes import client as nppes_client
from ...infrastructure.searxng import client as searxng_client
from ...infrastructure.cache import cache
from ...infrastructure.logging import get_logger


logger = get_logger(__name__)


def _cache_key(query: SearchQuery) -> str:
    """Generate cache key from query."""
    query_dict = query.model_dump(exclude_none=True)
    query_json = json.dumps(query_dict, sort_keys=True)
    return f"provider_search:{hashlib.md5(query_json.encode()).hexdigest()}"


async def execute(query: SearchQuery) -> ProviderSearchResult:
    # Check cache
    cache_key = _cache_key(query)
    cached = cache.get(cache_key)
    if cached is not None:
        logger.info("cache_hit", cache_key=cache_key)
        return cached
    
    logger.info("search_started", query=query.model_dump())
    nppes_results = await nppes_client.search(
        first_name=query.first_name,
        last_name=query.last_name,
        organization_name=query.organization_name,
        city=query.city,
        state=query.state,
        postal_code=query.postal_code,
        taxonomy=query.taxonomy,
        limit=query.limit,
    )

    providers: List[Provider] = []
    for item in nppes_results:
        basic = item.get("basic", {})
        addresses = item.get("addresses", [])
        address = addresses[0] if addresses else {}
        taxonomy = (item.get("taxonomies") or [{}])[0]
        first = basic.get("first_name")
        last = basic.get("last_name")
        org = basic.get("organization_name")
        display_name = " ".join([p for p in [first, last] if p]) if (first or last) else (org or "")

        website = None
        if display_name:
            web_results = await searxng_client.search(
                f"{display_name} {address.get('city','')} {address.get('state','')}",
                categories="general",
                num_results=3,
            )
            if web_results:
                website = web_results[0].get("url")

        providers.append(
            Provider(
                npi=str(item.get("number")),
                enumeration_type=item.get("enumeration_type", "NPI-1"),
                first_name=first,
                last_name=last,
                organization_name=org,
                city=address.get("city"),
                state=address.get("state"),
                postal_code=address.get("postal_code"),
                taxonomy=taxonomy.get("desc"),
                website=website,
                confidence=0.0,
            )
        )

    result = ProviderSearchResult(query=query, providers=providers)
    
    # Cache result
    cache.set(cache_key, result)
    logger.info("search_completed", providers_count=len(providers))
    
    return result


