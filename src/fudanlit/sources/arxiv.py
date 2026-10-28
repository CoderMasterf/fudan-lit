"""arXiv API：https://export.arxiv.org/api/query"""
from __future__ import annotations

import xml.etree.ElementTree as ET

from ..models import Author, Paper
from .base import BaseSource

ATOM = {"a": "http://www.w3.org/2005/Atom"}


class ArxivSource(BaseSource):
    name = "arxiv"
    base = "https://export.arxiv.org/api/query"

    def search(self, query: str, limit: int = 50) -> list[Paper]:
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": min(limit, 100),
        }
        self.limiter.wait()
        resp = self.session.get(self.base, params=params, timeout=30)
        resp.raise_for_status()

        root = ET.fromstring(resp.content)
        out: list[Paper] = []
        for entry in root.findall("a:entry", ATOM):
            title = " ".join((entry.findtext("a:title", "", ATOM) or "").split())
            abstract = " ".join((entry.findtext("a:summary", "", ATOM) or "").split())
            authors = [
                Author(name=" ".join(a.findtext("a:name", "", ATOM).split()))
                for a in entry.findall("a:author", ATOM)
            ]
            published = entry.findtext("a:published", "", ATOM) or ""
            year = int(published[:4]) if len(published) >= 4 else None

            pdf = None
            for link in entry.findall("a:link", ATOM):
                if link.get("type") == "application/pdf" or link.get("title") == "pdf":
                    pdf = link.get("href")
                    break

            out.append(
                Paper(
                    title=title,
                    authors=authors,
                    abstract=abstract,
                    year=year,
                    url=entry.findtext("a:id", "", ATOM),
                    pdf_url=pdf,
                    source=self.name,
                )
            )
        return out
