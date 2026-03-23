"""Networking helpers for the SmurfTracker compatibility shim."""

from __future__ import annotations

from urllib.parse import urlparse

import httpx

from shim.parser import WinsNotFoundError, extract_wins


class InvalidTargetUrlError(ValueError):
    """Raised when the requested URL is outside the supported RLStats scope."""


class ProfileNotFoundError(RuntimeError):
    """Raised when RLStats does not have the requested profile."""


class UpstreamServiceError(RuntimeError):
    """Raised when RLStats cannot be reached or returns an unusable page."""


_BROWSER_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/132.0.0.0 Safari/537.36"
    ),
}
_CHALLENGE_MARKERS = (
    "Just a moment...",
    "Attention Required! | Cloudflare",
    "__cf_chl_",
    "cf-challenge",
    "turnstile",
)


def validate_target_url(url: str) -> None:
    """Ensure the plugin can only resolve RLStats profile pages."""

    if not isinstance(url, str) or not url.strip():
        raise InvalidTargetUrlError("Missing url")

    parsed = urlparse(url)
    if parsed.scheme.lower() != "https":
        raise InvalidTargetUrlError("Only https://rlstats.net/profile/... URLs are supported")
    if parsed.netloc.lower() != "rlstats.net":
        raise InvalidTargetUrlError("Only https://rlstats.net/profile/... URLs are supported")
    if not parsed.path.startswith("/profile/"):
        raise InvalidTargetUrlError("Only https://rlstats.net/profile/... URLs are supported")


def _looks_like_challenge(html: str) -> bool:
    lowered = html.lower()
    return any(marker.lower() in lowered for marker in _CHALLENGE_MARKERS)


def fetch_profile_html(url: str, timeout: float = 15.0) -> str:
    """Fetch a RLStats profile page with browser-like headers."""

    validate_target_url(url)

    try:
        with httpx.Client(
            follow_redirects=True,
            headers=_BROWSER_HEADERS,
            max_redirects=5,
            timeout=timeout,
        ) as client:
            response = client.get(url)
    except httpx.TimeoutException as exc:
        raise UpstreamServiceError("Timed out while requesting RLStats") from exc
    except httpx.HTTPError as exc:
        raise UpstreamServiceError("Failed to request RLStats") from exc

    if response.status_code == 404:
        raise ProfileNotFoundError("RLStats profile not found")
    if response.status_code != 200:
        raise UpstreamServiceError(
            "RLStats returned unexpected status {status}".format(status=response.status_code)
        )

    html = response.text
    if _looks_like_challenge(html):
        raise UpstreamServiceError("RLStats returned a challenge page")
    return html


def resolve_wins(url: str) -> str:
    """Fetch and parse the wins string for a RLStats profile."""

    html = fetch_profile_html(url)
    return extract_wins(html)


__all__ = [
    "InvalidTargetUrlError",
    "ProfileNotFoundError",
    "UpstreamServiceError",
    "WinsNotFoundError",
    "fetch_profile_html",
    "resolve_wins",
    "validate_target_url",
]
