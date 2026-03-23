import os

import pytest

from shim.service import resolve_wins


@pytest.mark.skipif(
    os.environ.get("RLSTATS_LIVE_TESTS") != "1",
    reason="Set RLSTATS_LIVE_TESTS=1 to run live RLStats tests",
)
def test_resolve_wins_live_greenhollows() -> None:
    assert resolve_wins("https://rlstats.net/profile/Epic/greenhollows") == "9,352"
