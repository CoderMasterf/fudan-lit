from fudanlit.models import Author, Paper
from fudanlit.dedupe import dedupe


def test_dedupe_by_doi_merges_fields():
    a = Paper(title="Same Paper", doi="10.1234/abc", authors=[Author(name="张三")])
    b = Paper(title="Same Paper (variant)", doi="10.1234/ABC", abstract="摘要", pdf_url="http://x.pdf")
    out = dedupe([a, b])
    assert len(out) == 1
    assert out[0].abstract == "摘要"
    assert out[0].pdf_url == "http://x.pdf"
    assert out[0].authors[0].name == "张三"


def test_dedupe_by_title_year_when_no_doi():
    a = Paper(title="Hello World", year=2020)
    b = Paper(title="  hello world  ", year=2020)
    out = dedupe([a, b])
    assert len(out) == 1


def test_dedupe_keeps_distinct():
    a = Paper(title="A", year=2020)
    b = Paper(title="B", year=2021)
    assert len(dedupe([a, b])) == 2
