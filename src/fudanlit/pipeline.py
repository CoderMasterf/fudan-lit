"""把多个关键词 × 多个数据源串起来，去重后返回。"""
from __future__ import annotations

from .dedupe import dedupe
from .models import Paper


def run_search(sources: list, keywords: list[str], limit: int) -> list[Paper]:
    papers: list[Paper] = []
    for kw in keywords:
        for src in sources:
            try:
                papers.extend(src.search(kw, limit))
            except Exception as exc:  # noqa: BLE001 —— 单个源失败不拖垮整体
                print(f"[warn] {src.name} 查询 {kw!r} 失败：{exc}")
    return dedupe(papers)
