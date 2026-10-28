"""导出 CSV / BibTeX / JSON。"""
from __future__ import annotations

import csv
import dataclasses
import json

from .models import Paper


def _authors(p: Paper) -> str:
    return "; ".join(a.name for a in p.authors)


def _esc(s: str) -> str:
    return (s or "").replace("{", "\\{").replace("}", "\\}")


def write(papers: list[Paper], path: str, fmt: str) -> str:
    if fmt == "csv":
        return _csv(papers, path)
    if fmt == "bibtex":
        return _bibtex(papers, path)
    if fmt == "json":
        return _json(papers, path)
    raise ValueError(f"未知导出格式 {fmt!r}")


def _csv(papers: list[Paper], path: str) -> str:
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["title", "authors", "year", "doi", "venue", "abstract", "url", "pdf_url", "source"])
        for p in papers:
            w.writerow([p.title, _authors(p), p.year, p.doi, p.venue, p.abstract, p.url, p.pdf_url, p.source])
    return path


def _bibtex(papers: list[Paper], path: str) -> str:
    lines: list[str] = []
    for i, p in enumerate(papers):
        key = f"{p.source or 'misc'}{p.year or 'na'}{i + 1}"
        lines.append(f"@misc{{{key},")
        if p.title:
            lines.append(f"  title = {{{_esc(p.title)}}},")
        if p.authors:
            lines.append(f"  author = {{{_esc(' and '.join(a.name for a in p.authors))}}},")
        if p.year:
            lines.append(f"  year = {{{p.year}}},")
        if p.doi:
            lines.append(f"  doi = {{{_esc(p.doi)}}},")
        if p.venue:
            lines.append(f"  journal = {{{_esc(p.venue)}}},")
        if p.url:
            lines.append(f"  url = {{{_esc(p.url)}}},")
        if p.abstract:
            lines.append(f"  abstract = {{{_esc(p.abstract)}}},")
        lines.append("}")
        lines.append("")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def _json(papers: list[Paper], path: str) -> str:
    with open(path, "w", encoding="utf-8") as f:
        json.dump([dataclasses.asdict(p) for p in papers], f, ensure_ascii=False, indent=2)
    return path
