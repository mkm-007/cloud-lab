from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ServiceStore:
    """In-memory state for demo sessions and ingested events."""

    sessions: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    request_count: int = 0

    def seed_sessions(self) -> None:
        if self.sessions:
            return
        self.sessions = [
            {
                "session_id": "gfn-001",
                "region": "us-west",
                "status": "streaming",
                "latency_ms": 18,
            },
            {
                "session_id": "gfn-002",
                "region": "eu-central",
                "status": "streaming",
                "latency_ms": 24,
            },
            {
                "session_id": "gfn-003",
                "region": "ap-south",
                "status": "idle",
                "latency_ms": 31,
            },
        ]

    def record_request(self) -> None:
        self.request_count += 1

    def add_event(self, payload: dict[str, Any]) -> dict[str, Any]:
        event = {
            "event_id": f"evt-{len(self.events) + 1:03d}",
            "received_at": datetime.now(timezone.utc).isoformat(),
            **payload,
        }
        self.events.append(event)
        return event

    def active_sessions(self) -> int:
        return sum(1 for s in self.sessions if s["status"] == "streaming")
