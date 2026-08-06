"""Home Assistant REST 客户端封装。

端点（官方 REST API，Bearer Long-Lived Access Token）：
  - GET  /api/states/{entity_id}            查询单个实体状态
  - POST /api/services/{domain}/{service}   调用服务（如 light/turn_on）

错误统一抛 RuntimeError，message 里带 HA 状态码和响应摘要，
方便模型读取后直接向用户解释。
"""
from __future__ import annotations

from typing import Any

import httpx


class HomeAssistantClient:
    """Home Assistant REST API 的轻量异步客户端。"""

    def __init__(self, base_url: str, token: str, timeout: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/") + "/api"
        self.timeout = timeout
        self._headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        self._client: httpx.AsyncClient | None = None

    async def _http(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def close(self) -> None:
        """应用退出时释放连接池。"""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def get_state(self, entity_id: str) -> dict[str, Any]:
        """GET /api/states/{entity_id} -> 单个 state 对象。"""
        client = await self._http()
        resp = await client.get(
            f"{self.base_url}/states/{entity_id}", headers=self._headers
        )
        return self._handle(resp)

    async def call_service(
        self, domain: str, service: str, data: dict[str, Any] | None = None
    ) -> Any:
        """POST /api/services/{domain}/{service} -> 变更后的 state 列表（JSON 数组）。"""
        client = await self._http()
        resp = await client.post(
            f"{self.base_url}/services/{domain}/{service}",
            headers=self._headers,
            json=data or {},
        )
        return self._handle(resp)

    async def ping(self) -> bool:
        """GET /api/ 认证探活，供 /health 使用。"""
        try:
            client = await self._http()
            resp = await client.get(self.base_url, headers=self._headers)
            return resp.is_success
        except httpx.HTTPError:
            return False

    def _handle(self, resp: httpx.Response) -> Any:
        if resp.is_success:
            return resp.json() if resp.content else {"ok": True}
        detail = resp.text[:500]
        raise RuntimeError(
            f"Home Assistant API {resp.status_code} {resp.request.method} "
            f"{resp.request.url}: {detail}"
        )
