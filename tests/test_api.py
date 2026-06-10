from fastapi.testclient import TestClient

from cloudlab.app import app, store

client = TestClient(app)


def setup_function():
    store.events.clear()
    store.request_count = 0
    store.seed_sessions()


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_list_sessions():
    resp = client.get("/api/v1/sessions")
    body = resp.json()
    assert resp.status_code == 200
    assert body["count"] == 3
    assert body["sessions"][0]["session_id"] == "gfn-001"


def test_ingest_event():
    resp = client.post(
        "/api/v1/events",
        json={"session_id": "gfn-001", "event_type": "frame_upload", "latency_ms": 22},
    )
    assert resp.status_code == 201
    assert resp.json()["event_type"] == "frame_upload"


def test_ingest_unknown_session_returns_404():
    resp = client.post(
        "/api/v1/events",
        json={"session_id": "missing", "event_type": "error", "latency_ms": 10},
    )
    assert resp.status_code == 404


def test_metrics_prometheus_format():
    client.get("/health")
    client.post(
        "/api/v1/events",
        json={"session_id": "gfn-002", "event_type": "heartbeat", "latency_ms": 15},
    )
    resp = client.get("/metrics")
    text = resp.text
    assert resp.status_code == 200
    assert "cloud_requests_total" in text
    assert "cloud_active_sessions 2" in text
    assert "cloud_events_ingested 1" in text
