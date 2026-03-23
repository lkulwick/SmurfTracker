"""HTML parsing helpers for extracting RLStats wins."""

from __future__ import annotations

import re

from bs4 import BeautifulSoup


class WinsNotFoundError(ValueError):
    """Raised when the wins field cannot be extracted from RLStats HTML."""


_STATS_SECTION_RE = re.compile(
    r"<section[^>]+id=[\"']stats[\"'][\s\S]*?</section>",
    re.IGNORECASE,
)
_TD_WINS_RE = re.compile(r"^\s*([\d,]+)\s+Wins\s*$", re.IGNORECASE)
_SECTION_WINS_RE = re.compile(
    r"<td>\s*([\d,]+)\s+Wins\s*</td>",
    re.IGNORECASE,
)


def _extract_stats_section(html: str) -> str:
    match = _STATS_SECTION_RE.search(html)
    if match is None:
        raise WinsNotFoundError("RLStats stats section not found")
    return match.group(0)


def _extract_with_soup(stats_html: str) -> str | None:
    soup = BeautifulSoup(stats_html, "html.parser")
    containers = soup.select("div.block-stats") or [soup]

    for container in containers:
        for cell in container.find_all("td"):
            text = cell.get_text(" ", strip=True)
            match = _TD_WINS_RE.match(text)
            if match is not None:
                return match.group(1)

    return None


def _extract_with_regex(stats_html: str) -> str | None:
    match = _SECTION_WINS_RE.search(stats_html)
    if match is None:
        return None
    return match.group(1)


def extract_wins(html: str) -> str:
    """Extract the total wins string from a RLStats profile page."""

    if not isinstance(html, str) or not html.strip():
        raise WinsNotFoundError("RLStats HTML payload is empty")

    stats_html = _extract_stats_section(html)
    wins = _extract_with_soup(stats_html) or _extract_with_regex(stats_html)
    if wins is None:
        raise WinsNotFoundError("RLStats wins field not found")
    return wins
