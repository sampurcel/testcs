#!/usr/bin/env python3
"""Sync correlation rule definitions with CrowdStrike API.

This script reads a JSON file containing correlation rules and
submits them to the CrowdStrike Falcon API using credentials
provided via environment variables.

It is a simplified example based on the CrowdStrike detection-as-code
sample and is intended for use in GitHub Actions.
"""
import json
import os
import sys
from typing import Any, List

try:
    from falconpy import APIHarness
except Exception:  # pragma: no cover - library may not be installed during tests
    APIHarness = None


def load_rules(path: str) -> List[Any]:
    """Load rule definitions from *path*."""
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def submit_rules(rules: List[Any], base_url: str) -> None:
    """Submit *rules* to the CrowdStrike API."""
    if APIHarness is None:
        print("falconpy is not installed; displaying rules instead of submitting:")
        for rule in rules:
            print(json.dumps(rule, indent=2))
        return

    client_id = os.environ.get("FALCON_CLIENT_ID")
    client_secret = os.environ.get("FALCON_CLIENT_SECRET")
    cid = os.environ.get("FALCON_CID")
    if not all([client_id, client_secret, cid]):
        raise RuntimeError("Missing required CrowdStrike credentials")

    falcon = APIHarness(client_id=client_id, client_secret=client_secret, base_url=base_url)

    for rule in rules:
        body = {"cid": cid, **rule}
        falcon.command("POST", "/detects/entities/rules/v1", body=body)
        print(f"Submitted rule: {rule.get('name')}")


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print("Usage: sync_detections.py <rules.json> [base_url]", file=sys.stderr)
        return 1

    rules_path = argv[1]
    base_url = argv[2] if len(argv) > 2 else "https://api.crowdstrike.com"
    rules = load_rules(rules_path)
    submit_rules(rules, base_url)
    return 0


if __name__ == "__main__":  # pragma: no cover - command line entry
    raise SystemExit(main(sys.argv))
