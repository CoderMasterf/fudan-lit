"""数据源基类：统一查询接口 + 礼貌速率限制。"""
from __future__ import annotations

import time
from abc import ABC, abstractmethod

from ..models import Paper


class RateLimiter:
    """简单的串行限速器，避免打爆公共 API。"""

    def __init__(self, min_interval: float = 1.0):
        self.min_interval = min_interval
        self._last = 0.0

    def wait(self) -> None:
        now = time.monotonic()
        gap = now - self._last
        if gap < self.min_interval:
            time.sleep(self.min_interval - gap)
        self._last = time.monotonic()


class BaseSource(ABC):
    """所有数据源的公共骨架，子类只需实现 search()。"""

    name = "base"

    def __init__(self, session, mailto: str = "", **kwargs):
        self.session = session
        self.mailto = mailto
        self.limiter = RateLimiter()

    @abstractmethod
    def search(self, query: str, limit: int = 50) -> list[Paper]:
        """按关键词检索，返回 Paper 列表。"""
