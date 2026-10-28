"""按 DOI / 标题+年份 去重，并合并缺失字段。"""
from __future__ import annotations

from collections import OrderedDict

from .models import Paper


def dedupe(papers: list[Paper]) -> list[Paper]:
    seen: "OrderedDict[str, Paper]" = OrderedDict()
    for p in papers:
        k = p.key()
        if k not in seen:
            seen[k] = p
            continue
        existing = seen[k]
        # 用后面来源补前面缺的字段
        existing.abstract = existing.abstract or p.abstract
        existing.pdf_url = existing.pdf_url or p.pdf_url
        existing.venue = existing.venue or p.venue
        existing.url = existing.url or p.url
        if not existing.authors and p.authors:
            existing.authors = p.authors
    return list(seen.values())
