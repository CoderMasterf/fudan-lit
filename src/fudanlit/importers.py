"""订阅库导出文件导入：RIS / EndNote tagged / EndNote XML。

CNKI、WoS、Scopus 等订阅库没法稳定、无风险地在线抓取，但都支持「导出」成
RIS 或 EndNote 格式文件。把这些文件喂给 `fudan-lit import`，就能和开放源
结果合并去重、统一导出。这条通道既绕开了反爬，也完全落在订阅条款内。
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

from .models import Author, Paper


def import_files(paths: list[str]) -> list[Paper]:
    papers: list[Paper] = []
    for p in paths:
        text = Path(p).read_text(encoding="utf-8", errors="replace")
        low = text.lstrip().lower()
        if low.startswith("<") and "record" in low[:500]:
            papers.extend(_parse_endnote_xml(text))
        elif "%0" in text[:2000] or re.search(r"(?m)^%0 ", text):
            papers.extend(_parse_endnote_tagged(text))
        else:
            papers.extend(_parse_ris(text))
    return papers


def _parse_ris(text: str) -> list[Paper]:
    papers: list[Paper] = []
    for rec in re.split(r"(?m)^ER\s*-\s*$", text):
        fields: dict[str, list[str]] = {}
        for line in rec.splitlines():
            m = re.match(r"^([A-Z0-9]{2})\s+-\s?(.*)$", line)
            if not m:
                continue
            fields.setdefault(m.group(1), []).append(m.group(2).strip())

        title = " ".join(fields.get("TI", [])).strip()
        if not title and not fields.get("DO"):
            continue

        year = None
        if fields.get("PY"):
            m = re.search(r"\d{4}", fields["PY"][0])
            if m:
                year = int(m.group())

        papers.append(
            Paper(
                title=title,
                authors=[Author(name=a) for a in fields.get("AU", []) if a],
                abstract="\n".join(fields.get("AB", [])).strip() or None,
                year=year,
                doi=(fields.get("DO") or [None])[0],
                url=(fields.get("UR") or [None])[0],
                venue=" ".join(fields.get("JO", []) + fields.get("T2", [])).strip() or None,
                source="import",
            )
        )
    return papers


def _parse_endnote_tagged(text: str) -> list[Paper]:
    papers: list[Paper] = []
    for rec in re.split(r"\n\s*\n", text):
        fields: dict[str, list[str]] = {}
        for line in rec.splitlines():
            m = re.match(r"^%([A-Z0-9])\s+(.*)$", line)
            if not m:
                continue
            fields.setdefault(m.group(1), []).append(m.group(2).strip())

        title = " ".join(fields.get("T", [])).strip()
        if not title:
            continue

        year = None
        if fields.get("D"):
            m = re.search(r"\d{4}", fields["D"][0])
            if m:
                year = int(m.group())

        papers.append(
            Paper(
                title=title,
                authors=[Author(name=a) for a in fields.get("A", []) if a],
                abstract="\n".join(fields.get("X", [])).strip() or None,
                year=year,
                doi=(fields.get("R") or [None])[0],
                url=(fields.get("U") or [None])[0],
                venue=" ".join(fields.get("J", [])).strip() or None,
                source="import",
            )
        )
    return papers


def _findtext(el: ET.Element, tag: str) -> str | None:
    """在子树里按标签找第一个非空文本。"""
    for e in el.iter():
        if e.tag.split("}")[-1] == tag and e.text and e.text.strip():
            return e.text.strip()
    return None


def _parse_endnote_xml(text: str) -> list[Paper]:
    root = ET.fromstring(text)
    papers: list[Paper] = []
    for rec in root.iter("record"):
        title = _findtext(rec, "title")
        if not title:
            continue
        authors = [Author(name=a) for a in rec.iter("author") if a.text and a.text.strip()]
        year = None
        y = _findtext(rec, "year")
        if y:
            m = re.search(r"\d{4}", y)
            if m:
                year = int(m.group())
        papers.append(
            Paper(
                title=title,
                authors=authors,
                abstract=_findtext(rec, "abstract"),
                year=year,
                doi=_findtext(rec, "electronic-resource-num"),
                venue=_findtext(rec, "full-title"),
                source="import",
            )
        )
    return papers
