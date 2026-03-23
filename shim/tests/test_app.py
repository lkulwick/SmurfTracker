from fastapi.testclient import TestClient

import shim.app as app_module
from shim.app import app
from shim.parser import WinsNotFoundError
from shim.service import InvalidTargetUrlError, ProfileNotFoundError, UpstreamServiceError


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_v1_success_matches_plugin_contract(monkeypatch) -> None:
    monkeypatch.setattr(app_module, "resolve_wins", lambda url: "9,352")

    response = client.post(
        "/v1",
        json={
            "cmd": "request.get",
            "url": "https://rlstats.net/profile/Epic/greenhollows",
            "maxTimeout": 60000,
        },
    )

    assert response.status_code == 200
    assert response.json() == {"wins": "9,352"}


def test_v1_rejects_invalid_json() -> None:
    response = client.post(
        "/v1",
        content="{broken",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid JSON payload"


def test_v1_rejects_wrong_cmd() -> None:
    response = client.post(
        "/v1",
        json={
            "cmd": "request.post",
            "url": "https://rlstats.net/profile/Epic/greenhollows",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Unsupported cmd"


def test_v1_rejects_missing_url() -> None:
    response = client.post("/v1", json={"cmd": "request.get"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Missing url"


def test_v1_maps_invalid_target_to_400(monkeypatch) -> None:
    monkeypatch.setattr(
        app_module,
        "resolve_wins",
        lambda url: (_ for _ in ()).throw(
            InvalidTargetUrlError("Only https://rlstats.net/profile/... URLs are supported")
        ),
    )

    response = client.post(
        "/v1",
        json={
            "cmd": "request.get",
            "url": "https://example.com/profile/test",
        },
    )

    assert response.status_code == 400


def test_v1_maps_profile_not_found_to_404(monkeypatch) -> None:
    monkeypatch.setattr(
        app_module,
        "resolve_wins",
        lambda url: (_ for _ in ()).throw(ProfileNotFoundError("RLStats profile not found")),
    )

    response = client.post(
        "/v1",
        json={
            "cmd": "request.get",
            "url": "https://rlstats.net/profile/Epic/does-not-exist",
        },
    )

    assert response.status_code == 404


def test_v1_maps_missing_wins_to_404(monkeypatch) -> None:
    monkeypatch.setattr(
        app_module,
        "resolve_wins",
        lambda url: (_ for _ in ()).throw(WinsNotFoundError("RLStats wins field not found")),
    )

    response = client.post(
        "/v1",
        json={
            "cmd": "request.get",
            "url": "https://rlstats.net/profile/Epic/greenhollows",
        },
    )

    assert response.status_code == 404


def test_v1_maps_upstream_errors_to_502(monkeypatch) -> None:
    monkeypatch.setattr(
        app_module,
        "resolve_wins",
        lambda url: (_ for _ in ()).throw(UpstreamServiceError("Timed out while requesting RLStats")),
    )

    response = client.post(
        "/v1",
        json={
            "cmd": "request.get",
            "url": "https://rlstats.net/profile/Epic/greenhollows",
        },
    )

    assert response.status_code == 502
