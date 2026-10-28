"""统一数据模型：所有来源（在线 API 或导入文件）都归一成 Paper。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Author:
    name: str
    orcid: Optional[str] = None
    affiliation: Optional[str] = None


@dataclass
class Paper:
    title: str
    authors: list[Author] = field(default_factory=list)
    abstract: Optional[str] = None
    year: Optional[int] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    pdf_url: Optional[str] = None
    venue: Optional[str] = None
    source: str = ""
    keywords: Optional[str] = None
    extra: dict = field(default_factory=dict)

    def key(self) -> str:
        """去重主键：有 DOI 用 DOI，否则用标题 + 年份。"""
        if self.doi:
            return f"doi:{self.doi.lower()}"
        title = self.title.strip().lower()
        return f"title:{title}|{self.year or ''}"
