#!/usr/bin/env python3
"""Smoke-check the REST service and print honest stats for resume bullets."""

from fastapi.testclient import TestClient

from cloudlab.app import app, store


def main() -> None:
    store.events.clear()
    store.request_count = 0
    store.seed_sessions()

    client = TestClient(app)
    client.get("/health")
    client.get("/api/v1/sessions")
    client.post(
        "/api/v1/events",
        json={"session_id": "gfn-001", "event_type": "frame_upload", "latency_ms": 18},
    )
    metrics = client.get("/metrics").text

    print(
        {
            "endpoints": 4,
            "seed_sessions": len(store.sessions),
            "active_streaming": store.active_sessions(),
            "events_ingested": len(store.events),
            "metrics_sample": metrics.strip().split("\n")[-1],
        }
    )


if __name__ == "__main__":
    main()
