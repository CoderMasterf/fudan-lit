"""Crossref REST API：https://api.crossref.org"""
from __future__ import annotations

from ..models import Author, Paper
from .base import BaseSource


class CrossrefSource(BaseSource):
    name = "crossref"
    base = "https://api.crossref.org/works"

    def search(self, query: str, limit: int = 50) -> list[Paper]:
        params: dict = {
            "query": query,
            "rows": min(limit, 1000),
            "select": "DOI,title,author,abstract,issued,URL,link,container-title",
        }
        if self.mailto:
            params["mailto"] = self.mailto

        self.limiter.wait()
        resp = self.session.get(self.base, params=params, timeout=30)
        resp.raise_for_status()

        items = resp.json()["message"]["items"]
        out: list[Paper] = []
        for it in items:
            title = (it.get("title") or [""])[0]
            if not title:
                continue
            authors = [
                Author(name=f"{a.get('given', '')} {a.get('family', '')}".strip())
                for a in it.get("author", [])
            ]
            year = None
            issued = it.get("issued", {}).get("date-parts", [[None]])
            if issued and issued[0] and issued[0][0]:
                year = int(issued[0][0])

            pdf = None
            for link in it.get("link", []):
                if link.get("URL", "").endswith(".pdf"):
                    pdf = link["URL"]
                    break

            out.append(
                Paper(
                    title=title,
                    authors=authors,
                    abstract=it.get("abstract"),
                    year=year,
                    doi=it.get("DOI"),
                    url=it.get("URL"),
                    pdf_url=pdf,
                    venue=(it.get("container-title") or [""])[0],
                    source=self.name,
                )
            )
        return out
