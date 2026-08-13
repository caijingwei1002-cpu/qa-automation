#!/usr/bin/env python3
"""Validate the long-lived structure and generated plan of this repository."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ASSETS = {
    "test-projects/01-todomvc-ui",
    "test-projects/02-saucedemo-ui",
    "test-projects/03-restful-booker-api",
    "test-projects/04-petstore-performance",
}
LEGACY_DIRS = {
    "01-todomvc-ui",
    "02-saucedemo-ui",
    "03-restful-booker-api",
    "04-petstore-performance",
    "tests",
}


def load_json(relative: str) -> dict:
    path = ROOT / relative
    return json.loads(path.read_text(encoding="utf-8-sig"))


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []

    for relative in ["README.md", ".gitignore", ".env.example", "config/targets.json", "daily-plan.json", "curriculum.json"]:
        if not (ROOT / relative).is_file():
            fail(errors, f"missing required file: {relative}")

    for relative in EXPECTED_ASSETS:
        if not (ROOT / relative).is_dir():
            fail(errors, f"missing test asset directory: {relative}")
        if not (ROOT / relative / "README.md").is_file():
            fail(errors, f"missing test asset README: {relative}/README.md")

    for relative in LEGACY_DIRS:
        if (ROOT / relative).exists():
            fail(errors, f"legacy top-level project directory still exists: {relative}")

    targets = load_json("config/targets.json")
    registered_assets = {
        item["test_asset_directory"] for item in targets.get("targets", {}).values()
    }
    if registered_assets != EXPECTED_ASSETS:
        fail(errors, f"target registry does not match test assets: {sorted(registered_assets)}")

    daily_plan = load_json("daily-plan.json")
    days = daily_plan.get("days", [])
    if daily_plan.get("core_days") != 182 or len(days) != 182:
        fail(errors, f"daily plan must contain 182 days, got {len(days)}")

    for item in days:
        for field in ("project", "file", "run"):
            value = str(item.get(field, ""))
            if "test-projects/" in value and "test-projects/test-projects/" in value:
                fail(errors, f"duplicated path in day {item.get('day')} {field}: {value}")
            if any(value.startswith(f"{legacy}/") for legacy in LEGACY_DIRS):
                fail(errors, f"legacy path in day {item.get('day')} {field}: {value}")

    nested_git = [
        path for path in ROOT.rglob(".git") if path != ROOT / ".git"
    ]
    if nested_git:
        fail(errors, f"nested Git directories found: {nested_git}")

    if errors:
        print("Repository validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Repository validation passed: structure, targets, generated plan, and Git boundaries are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
