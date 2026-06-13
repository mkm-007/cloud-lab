from pathlib import Path

from cloudlab.cli import run_cli
from cloudlab.secrets import SecretsStore


def test_list_secrets_for_project():
    store = SecretsStore()
    store.seed()
    rows = store.list_for_project("web-app")
    assert len(rows) == 3
    assert rows[0]["name"] == "DATABASE_URL"


def test_get_secret_value():
    store = SecretsStore()
    store.seed()
    secret = store.get("API_KEY", "web-app")
    assert secret is not None
    assert secret["value"].startswith("sk-demo")


def test_mount_env_writes_local_file(tmp_path):
    store = SecretsStore()
    store.seed()
    out = tmp_path / ".env.local"
    meta = store.mount_env("web-app", out)
    assert meta["secrets_mounted"] == 3
    text = out.read_text()
    assert "DATABASE_URL=" in text
    assert "API_KEY=" in text


def test_cli_list_command():
    result = run_cli(["list", "--project", "auth"])
    assert result["count"] == 2


def test_cli_get_command():
    result = run_cli(["get", "--name", "JWT_SIGNING_KEY", "--project", "auth"])
    assert result["name"] == "JWT_SIGNING_KEY"


def test_cli_mount_env_command(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = run_cli(["mount-env", "--project", "billing", "--output", ".env.billing"])
    assert result["secrets_mounted"] == 1
    assert Path(".env.billing").exists()


def test_secrets_api_list():
    from fastapi.testclient import TestClient

    from cloudlab.app import app

    client = TestClient(app)
    resp = client.get("/api/v1/secrets", params={"project": "web-app"})
    body = resp.json()
    assert resp.status_code == 200
    assert body["count"] == 3


def test_secrets_api_get_not_found():
    from fastapi.testclient import TestClient

    from cloudlab.app import app

    client = TestClient(app)
    resp = client.get("/api/v1/secrets/MISSING")
    assert resp.status_code == 404
