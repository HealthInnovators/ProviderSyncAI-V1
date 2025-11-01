import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from .settings import settings


_timeout = httpx.Timeout(settings.request_timeout_seconds)


def _client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=_timeout)


@retry(stop=stop_after_attempt(max(1, settings.http_max_retries + 1)), wait=wait_exponential(multiplier=0.2, min=0.2, max=2))
async def get(url: str, params: dict | None = None, headers: dict | None = None) -> httpx.Response:
    async with _client() as client:
        resp = await client.get(url, params=params, headers=headers)
        resp.raise_for_status()
        return resp


@retry(stop=stop_after_attempt(max(1, settings.http_max_retries + 1)), wait=wait_exponential(multiplier=0.2, min=0.2, max=2))
async def post(url: str, json: dict | None = None, headers: dict | None = None) -> httpx.Response:
    async with _client() as client:
        resp = await client.post(url, json=json, headers=headers)
        resp.raise_for_status()
        return resp


