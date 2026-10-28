"""OpenAlex API：https://api.openalex.org"""
from __future__ import annotations

from ..models import Author, Paper
from .base import BaseSource


class OpenAlexSource(BaseSource):
    name = "openalex"
    base = "https://api.openalex.org/works"

    def search(self, query: str, limit: int = 50) -> list[Paper]:
        params: dict = {"search": query, "per-page": min(limit, 200)}
        if self.mailto:
            params["mailto"] = self.mailto

        self.limiter.wait()
        resp = self.session.get(self.base, params=params, timeout=30)
        resp.raise_for_status()

        out: list[Paper] = []
        for w in resp.json().get("results", []):
            title = w.get("title") or ""
            if not title:
                continue

            authors: list[Author] = []
            for a in w.get("authorships", []):
                au = a.get("author") or {}
                insts = a.get("institutions") or []
                authors.append(
                    Author(
                        name=au.get("display_name", ""),
                        orcid=au.get("orcid"),
                        affiliation=insts[0].get("display_name") if insts else None,
                    )
                )

            doi = None
            if w.get("doi"):
                doi = w["doi"].removeprefix("https://doi.org/")

            oa = w.get("open_access") or {}
            pdf = None
            if oa.get("is_oa") and oa.get("oa_url"):
                pdf = oa["oa_url"]

            venue = None
            loc = w.get("primary_location") or {}
            src = loc.get("source") or {}
            if src.get("display_name"):
                venue = src["display_name"]

            out.append(
                Paper(
                    title=title,
                    authors=authors,
                    abstract=None,
                    year=w.get("publication_year"),
                    doi=doi,
                    url=w.get("doi"),
                    pdf_url=pdf,
                    venue=venue,
                    source=self.name,
                )
            )
        return out
