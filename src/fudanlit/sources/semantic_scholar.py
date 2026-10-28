"""Semantic Scholar Graph API：https://api.semanticscholar.org"""
from __future__ import annotations

from ..models import Author, Paper
from .base import BaseSource, RateLimiter


class SemanticScholarSource(BaseSource):
    name = "semantic_scholar"
    base = "https://api.semanticscholar.org/graph/v1/paper/search"

    def __init__(self, session, mailto: str = "", api_key: str = "", **kwargs):
        super().__init__(session, mailto=mailto, **kwargs)
        self.api_key = api_key
        # 有 key 时官方允许到约 100 req/s；无 key 保守用 1 req/s
        self.limiter = RateLimiter(0.05 if api_key else 1.0)

    def search(self, query: str, limit: int = 50) -> list[Paper]:
        fields = "title,authors,abstract,year,externalIds,openAccessPdf,url,venue"
        params = {"query": query, "limit": min(limit, 100), "fields": fields}
        headers = {"x-api-key": self.api_key} if self.api_key else {}

        self.limiter.wait()
        resp = self.session.get(self.base, params=params, headers=headers, timeout=30)
        resp.raise_for_status()

        out: list[Paper] = []
        for d in resp.json().get("data", []):
            title = d.get("title") or ""
            if not title:
                continue
            authors = [Author(name=a.get("name", "")) for a in d.get("authors", [])]
            external = d.get("externalIds") or {}
            pdf = (d.get("openAccessPdf") or {}).get("url")
            out.append(
                Paper(
                    title=title,
                    authors=authors,
                    abstract=d.get("abstract"),
                    year=d.get("year"),
                    doi=external.get("DOI"),
                    url=d.get("url"),
                    pdf_url=pdf,
                    venue=d.get("venue"),
                    source=self.name,
                )
            )
        return out
