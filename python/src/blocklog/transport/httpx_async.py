import asyncio

try:
    import httpx
except ModuleNotFoundError:  # pragma: no cover - exercised in local fallback mode
    httpx = None
    import requests
else:
    requests = None

from .auth import build_headers


class AsyncTransport:
    def __init__(self, *, base_url: str, api_key: str, timeout: float) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout) if httpx is not None else None

    async def request(self, method: str, path: str, *, json: dict | None = None, headers: dict[str, str] | None = None):
        if self.client is not None:
            response = await self.client.request(
                method,
                f"{self.base_url}{path}",
                json=json,
                headers=build_headers(self.api_key, headers),
            )
        else:
            response = await asyncio.to_thread(
                requests.request,
                method,
                f"{self.base_url}{path}",
                json=json,
                headers=build_headers(self.api_key, headers),
                timeout=self.timeout,
            )
        response.raise_for_status()
        return response.json()
