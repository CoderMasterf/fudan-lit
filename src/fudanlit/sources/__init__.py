"""数据源注册表。"""
from __future__ import annotations

from .arxiv import ArxivSource
from .crossref import CrossrefSource
from .openalex import OpenAlexSource
from .semantic_scholar import SemanticScholarSource

REGISTRY = {
    "crossref": CrossrefSource,
    "openalex": OpenAlexSource,
    "arxiv": ArxivSource,
    "semantic_scholar": SemanticScholarSource,
}


def make_sources(names: str, session, cfg: dict) -> list:
    """把逗号分隔的数据源名实例化成列表。"""
    out = []
    for raw in names.split(","):
        name = raw.strip().lower()
        cls = REGISTRY.get(name)
        if cls is None:
            print(f"[warn] 未知数据源 {raw!r}，跳过（可用：{', '.join(REGISTRY)}）")
            continue
        out.append(
            cls(
                session,
                mailto=cfg.get("mailto", ""),
                api_key=cfg.get("semantic_scholar_api_key", ""),
            )
        )
    return out
