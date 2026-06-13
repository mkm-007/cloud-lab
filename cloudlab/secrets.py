from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class SecretsStore:
    """In-memory vault for developer secrets — CLI and API demos."""

    items: list[dict[str, Any]] = field(default_factory=list)

    def seed(self) -> None:
        if self.items:
            return
        self.items = [
            {"name": "DATABASE_URL", "project": "web-app", "value": "postgres://localhost:5432/app"},
            {"name": "API_KEY", "project": "web-app", "value": "sk-demo-web-7f3a"},
            {"name": "STRIPE_SECRET", "project": "billing", "value": "sk_test_billing_9c21"},
            {"name": "JWT_SIGNING_KEY", "project": "auth", "value": "jwt-signing-demo-key"},
            {"name": "REDIS_URL", "project": "web-app", "value": "redis://localhost:6379/0"},
            {"name": "OAUTH_CLIENT_SECRET", "project": "auth", "value": "oauth-client-demo-secret"},
        ]

    def list_for_project(self, project: str | None = None) -> list[dict[str, str]]:
        rows = self.items if project is None else [i for i in self.items if i["project"] == project]
        return [{"name": r["name"], "project": r["project"]} for r in rows]

    def get(self, name: str, project: str | None = None) -> dict[str, str] | None:
        for item in self.items:
            if item["name"] == name and (project is None or item["project"] == project):
                return {"name": item["name"], "project": item["project"], "value": item["value"]}
        return None

    def mount_env(self, project: str, output: Path) -> dict[str, int | str]:
        secrets = [i for i in self.items if i["project"] == project]
        if not secrets:
            raise ValueError(f"no secrets for project: {project}")
        lines = [f"{s['name']}={s['value']}" for s in secrets]
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text("\n".join(lines) + "\n")
        return {"project": project, "secrets_mounted": len(secrets), "output": str(output)}

    def project_count(self) -> int:
        return len({i["project"] for i in self.items})
