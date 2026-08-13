#!/usr/bin/env python3
"""Validate the long-lived structure and generated plan of this repository."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_daily_plan import DAILY_METHOD, build_plan  # noqa: E402


EXPECTED_ASSETS = {
    "test-projects/01-todomvc-ui",
    "test-projects/02-saucedemo-ui",
    "test-projects/03-restful-booker-api",
    "test-projects/04-petstore-performance",
}
EXPECTED_TIMEBOX = DAILY_METHOD
REQUIRED_DAILY_FIELDS = (
    "title",
    "learn",
    "study",
    "practice",
    "deliverable",
    "file",
    "run",
    "done",
    "knowledge_check",
    "stretch",
    "evidence",
    "learning_output_link",
    "timebox",
)
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

    for relative in [
        "README.md",
        ".gitignore",
        ".env.example",
        "config/targets.json",
        "daily-plan.json",
        "DAILY-PLAN.md",
        "curriculum.json",
        "templates/daily-log.md",
        ".github/workflows/repository-validation.yml",
    ]:
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
    if daily_plan.get("session_minutes") != 90:
        fail(errors, f"daily plan session must be 90 minutes, got {daily_plan.get('session_minutes')}")
    if daily_plan.get("daily_method") != EXPECTED_TIMEBOX:
        fail(errors, "daily plan daily_method does not match the 20/50/15/5 learning loop")

    curriculum = load_json("curriculum.json")
    daily_output = curriculum.get("daily_output", {})
    if daily_output.get("time_box_minutes") != 90 or daily_output.get("timebox") != EXPECTED_TIMEBOX:
        fail(errors, "curriculum daily_output does not match the 20/50/15/5 learning loop")
    expected_days = build_plan()
    if days != expected_days:
        fail(errors, "daily-plan.json is out of sync with tools/build_daily_plan.py; regenerate it")
    phases = curriculum.get("phases", [])
    cursor = 0
    for phase in phases:
        phase_days = days[cursor : cursor + phase.get("days", 0)]
        if len(phase_days) != phase.get("days", 0):
            fail(errors, f"curriculum phase has an invalid day count: {phase.get('id')}")
            continue
        for plan_field, curriculum_field in (("phase", "name"), ("project", "project"), ("objective", "objective")):
            if any(item.get(plan_field) != phase.get(curriculum_field) for item in phase_days):
                fail(errors, f"curriculum phase {phase.get('id')} is out of sync for {curriculum_field}")
        cursor += phase.get("days", 0)
    if cursor != len(days):
        fail(errors, f"curriculum phase totals {cursor} days, expected {len(days)}")
    ongoing = curriculum.get("ongoing", {})
    for track in ongoing.get("tracks", []):
        for index, task in enumerate(track.get("tasks", []), start=1):
            if not isinstance(task, dict) or not all(task.get(field) for field in ("task", "learn", "deliverable", "file", "run")):
                fail(errors, f"ongoing track {track.get('name')} task {index} must define task, learn, deliverable, file, and run")
            elif "daily-log/" in task["file"] or "artifacts/" in task["file"]:
                fail(errors, f"ongoing track {track.get('name')} task {index} must point to a real output file")

    for expected_day, item in enumerate(days, start=1):
        missing = [field for field in REQUIRED_DAILY_FIELDS if field not in item]
        if missing:
            fail(errors, f"day {item.get('day', expected_day)} missing daily fields: {', '.join(missing)}")
            continue
        if item.get("day") != expected_day:
            fail(errors, f"daily plan day sequence mismatch at position {expected_day}")
        for field in REQUIRED_DAILY_FIELDS:
            if field == "timebox":
                continue
            if not isinstance(item[field], str) or not item[field].strip():
                fail(errors, f"day {item.get('day')} field is empty: {field}")
        if item.get("timebox") != EXPECTED_TIMEBOX:
            fail(errors, f"day {item.get('day')} has an invalid timebox")
        if item["learn"] not in item["study"]:
            fail(errors, f"day {item.get('day')} study does not explain learn")
        if item["deliverable"] not in item["practice"]:
            fail(errors, f"day {item.get('day')} practice does not produce deliverable")
        if item["learn"] not in item["knowledge_check"]:
            fail(errors, f"day {item.get('day')} knowledge check does not check learn")
        for linked_value in (item["learn"], item["deliverable"], item["done"]):
            if linked_value not in item["learning_output_link"]:
                fail(errors, f"day {item.get('day')} learning_output_link is incomplete")
        expected_evidence = f"artifacts/day-{expected_day:03d}/"
        if item["evidence"] != expected_evidence:
            fail(errors, f"day {item.get('day')} evidence path must be {expected_evidence}")
        for field in ("project", "file", "run", "evidence"):
            value = str(item.get(field, ""))
            if "test-projects/" in value and "test-projects/test-projects/" in value:
                fail(errors, f"duplicated path in day {item.get('day')} {field}: {value}")
            if any(value.startswith(f"{legacy}/") for legacy in LEGACY_DIRS):
                fail(errors, f"legacy path in day {item.get('day')} {field}: {value}")

    log_dir = ROOT / "daily-log"
    for log_path in sorted(log_dir.glob("day-*.md")):
        try:
            log_day = int(log_path.stem.removeprefix("day-"))
        except ValueError:
            fail(errors, f"invalid daily log filename: {log_path.name}")
            continue
        if not 1 <= log_day <= len(days):
            continue
        log_text = log_path.read_text(encoding="utf-8")
        expected_evidence = f"artifacts/day-{log_day:03d}/"
        if expected_evidence not in log_text:
            fail(errors, f"daily log {log_path.name} does not reference {expected_evidence}")
        if "## 今日学习与产出" not in log_text:
            fail(errors, f"daily log {log_path.name} does not use the learning/output template")

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
