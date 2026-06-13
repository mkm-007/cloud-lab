from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from cloudlab.secrets import SecretsStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="cloud-lab developer secrets CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    list_cmd = sub.add_parser("list", help="List secret names for a project")
    list_cmd.add_argument("--project", default=None)

    get_cmd = sub.add_parser("get", help="Fetch one secret value")
    get_cmd.add_argument("--name", required=True)
    get_cmd.add_argument("--project", default=None)

    mount_cmd = sub.add_parser("mount-env", help="Write project secrets to a local .env file")
    mount_cmd.add_argument("--project", required=True)
    mount_cmd.add_argument("--output", default=".env.local")

    return parser


def run_cli(argv: list[str] | None = None) -> dict:
    store = SecretsStore()
    store.seed()
    args = build_parser().parse_args(argv)

    if args.command == "list":
        rows = store.list_for_project(args.project)
        return {"secrets": rows, "count": len(rows)}
    if args.command == "get":
        secret = store.get(args.name, args.project)
        if secret is None:
            raise SystemExit(f"secret not found: {args.name}")
        return secret
    if args.command == "mount-env":
        return store.mount_env(args.project, Path(args.output))
    raise SystemExit(f"unknown command: {args.command}")


def main() -> None:
    result = run_cli()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
