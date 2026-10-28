"""命令行入口：search（在线抓）与 import（订阅库导出文件导入）。"""
from __future__ import annotations

import argparse
import sys

import requests

from .config import load_config
from .dedupe import dedupe
from .export import write
from .pipeline import run_search
from .sources import make_sources

DEFAULT_SOURCES = "crossref,openalex,arxiv,semantic_scholar"
UA = "fudan-lit/0.1"


def _emit(papers, output: str, fmt: str) -> None:
    if fmt == "all":
        base = output.rsplit(".", 1)[0]
        for f in ("csv", "bibtex", "json"):
            print(f"  已导出 {write(papers, f'{base}.{f}', f)}")
    else:
        print(f"  已导出 {write(papers, output, fmt)}")


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(
        prog="fudan-lit",
        description="复旦订阅范围内文献元数据抓取（开放源在线抓 + 订阅库导出文件导入）",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="按关键词在线抓取元数据")
    s.add_argument("-k", "--keyword", action="append", required=True, help="关键词，可重复")
    s.add_argument("--sources", default=DEFAULT_SOURCES, help="逗号分隔的数据源")
    s.add_argument("--limit", type=int, default=50, help="每个源每个关键词取多少条")
    s.add_argument("-o", "--output", default="results.csv")
    s.add_argument("--format", default="csv", choices=["csv", "bibtex", "json", "all"])

    i = sub.add_parser("import", help="导入订阅库（CNKI/WoS/Scopus）导出的 RIS/EndNote 文件")
    i.add_argument("files", nargs="+", help="RIS / EndNote XML / EndNote tagged 文件")
    i.add_argument("-o", "--output", default="results.csv")
    i.add_argument("--format", default="csv", choices=["csv", "bibtex", "json", "all"])

    args = parser.parse_args(argv)
    cfg = load_config()

    if args.cmd == "search":
        session = requests.Session()
        session.headers["User-Agent"] = f"{UA} (mailto:{cfg['mailto'] or 'unset'})"
        sources = make_sources(args.sources, session, cfg)
        papers = run_search(sources, args.keyword, args.limit)
        for p in papers:
            p.keywords = "; ".join(args.keyword)
        print(f"共 {len(papers)} 篇（去重后）")
        _emit(papers, args.output, args.format)
        return 0

    if args.cmd == "import":
        from .importers import import_files

        papers = dedupe(import_files(args.files))
        print(f"共 {len(papers)} 篇（去重后）")
        _emit(papers, args.output, args.format)
        return 0

    parser.error("未知子命令")
    return 2
