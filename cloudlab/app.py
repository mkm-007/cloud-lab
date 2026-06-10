from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from cloudlab.store import ServiceStore

store = ServiceStore()
store.seed_sessions()

app = FastAPI(title="cloud-lab", version="0.1.0")


class EventIn(BaseModel):
    session_id: str = Field(min_length=1)
    event_type: str = Field(min_length=1)
    latency_ms: int = Field(ge=0, le=5000)


@app.middleware("http")
async def count_requests(request, call_next):
    store.record_request()
    return await call_next(request)


@app.get("/health")
def health():
    return {"status": "ok", "service": "cloud-lab"}


@app.get("/api/v1/sessions")
def list_sessions():
    return {"count": len(store.sessions), "sessions": store.sessions}


@app.post("/api/v1/events", status_code=201)
def ingest_event(event: EventIn):
    if not any(s["session_id"] == event.session_id for s in store.sessions):
        raise HTTPException(status_code=404, detail="session not found")
    created = store.add_event(event.model_dump())
    return created


@app.get("/metrics")
def metrics():
    lines = [
        "# HELP cloud_requests_total Total HTTP requests served",
        "# TYPE cloud_requests_total counter",
        f"cloud_requests_total {store.request_count}",
        "# HELP cloud_active_sessions Active streaming sessions",
        "# TYPE cloud_active_sessions gauge",
        f"cloud_active_sessions {store.active_sessions()}",
        "# HELP cloud_events_ingested Total events ingested",
        "# TYPE cloud_events_ingested counter",
        f"cloud_events_ingested {len(store.events)}",
    ]
    return "\n".join(lines) + "\n"
