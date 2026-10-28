import json
from pathlib import Path

from fudanlit.models import Author, Paper
from fudanlit.export import write


def test_export_json(tmp_path: Path):
    p = Paper(title="测试", authors=[Author(name="张三")], year=2021, doi="10.1/x", source="crossref")
    out = tmp_path / "out.json"
    write([p], str(out), "json")
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data[0]["title"] == "测试"
    assert data[0]["doi"] == "10.1/x"


def test_export_bibtex(tmp_path: Path):
    p = Paper(title="A {test}", year=2020, source="arxiv")
    out = tmp_path / "out.bib"
    write([p], str(out), "bibtex")
    text = out.read_text(encoding="utf-8")
    assert "@misc{" in text
    assert "\\{" in text


def test_export_csv(tmp_path: Path):
    p = Paper(title="T", authors=[Author(name="A")], year=2020, source="openalex")
    out = tmp_path / "out.csv"
    write([p], str(out), "csv")
    text = out.read_text(encoding="utf-8-sig")
    assert "title" in text
    assert "T" in text
