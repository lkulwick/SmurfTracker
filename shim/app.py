"""FastAPI app that preserves the existing SmurfTracker DLL contract."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from shim.parser import WinsNotFoundError
from shim.service import (
    InvalidTargetUrlError,
    ProfileNotFoundError,
    UpstreamServiceError,
    resolve_wins,
)


app = FastAPI(title="SmurfTracker Shim", docs_url=None, redoc_url=None)


def _read_request_payload(payload: object) -> str:
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Payload must be a JSON object")

    cmd = payload.get("cmd")
    if cmd != "request.get":
        raise HTTPException(status_code=400, detail="Unsupported cmd")

    url = payload.get("url")
    if not isinstance(url, str) or not url.strip():
        raise HTTPException(status_code=400, detail="Missing url")

    return url


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})


@app.post("/v1")
async def solve(request: Request) -> JSONResponse:
    try:
        payload = await request.json()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON payload") from exc

    url = _read_request_payload(payload)

    try:
        wins = resolve_wins(url)
    except InvalidTargetUrlError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except (ProfileNotFoundError, WinsNotFoundError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except UpstreamServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return JSONResponse(content={"wins": wins})
