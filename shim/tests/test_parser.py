from pathlib import Path

import pytest

import shim.parser as parser
from shim.parser import WinsNotFoundError, extract_wins


FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "rlstats_greenhollows_stats.html"


def test_extract_wins_from_fixture() -> None:
    html = FIXTURE_PATH.read_text(encoding="utf-8")

    assert extract_wins(html) == "9,352"


def test_extract_wins_falls_back_to_regex(monkeypatch) -> None:
    html = """
    <section id="stats">
      <div class="block-stats">
        <table>
          <tr><td>9,352 Wins</td></tr>
        </table>
      </div>
    </section>
    """

    monkeypatch.setattr(parser, "_extract_with_soup", lambda stats_html: None)

    assert parser.extract_wins(html) == "9,352"


def test_extract_wins_requires_stats_section() -> None:
    with pytest.raises(WinsNotFoundError):
        extract_wins("<html><body><p>no stats here</p></body></html>")
