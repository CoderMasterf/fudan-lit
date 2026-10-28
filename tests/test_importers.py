from fudanlit.importers import _parse_ris, _parse_endnote_tagged

RIS = """TY  - JOUR
TI  - Example Paper
AU  - Zhang, San
PY  - 2021
DO  - 10.1000/xyz
AB  - Some abstract.
UR  - https://doi.org/10.1000/xyz
ER  - 
"""

TAGGED = """%0 Journal Article
%A Li, Si
%T Another Paper
%J Test Journal
%D 2020
%R 10.1000/abc
%X An abstract here.
"""


def test_parse_ris():
    papers = _parse_ris(RIS)
    assert len(papers) == 1
    assert papers[0].title == "Example Paper"
    assert papers[0].year == 2021
    assert papers[0].doi == "10.1000/xyz"
    assert papers[0].authors[0].name == "Zhang, San"


def test_parse_endnote_tagged():
    papers = _parse_endnote_tagged(TAGGED)
    assert len(papers) == 1
    assert papers[0].title == "Another Paper"
    assert papers[0].year == 2020
    assert papers[0].doi == "10.1000/abc"
