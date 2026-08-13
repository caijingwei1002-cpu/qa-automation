#!/usr/bin/env python3
"""Small dependency-free MCP stdio server for the local QA learning lab."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


SERVER_NAME = "qa-learning-local"
SERVER_VERSION = "0.1.0"


def project_root(arguments: dict[str, Any] | None = None) -> Path:
    arguments = arguments or {}
    supplied = arguments.get("root") or os.environ.get("QA_LEARNING_ROOT")
    if supplied:
        return Path(str(supplied)).expanduser().resolve()
    return Path(__file__).resolve().parents[3]


def run_planner(arguments: dict[str, Any], command: str, *extra: str) -> dict[str, Any]:
    root = project_root(arguments)
    planner = root / "tools" / "plan_day.py"
    if not planner.exists():
        raise FileNotFoundError(f"learning planner not found: {planner}")
    child_env = os.environ.copy()
    child_env["PYTHONIOENCODING"] = "utf-8"
    completed = subprocess.run(
        [sys.executable, str(planner), command, *extra],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=child_env,
        check=False,
    )
    output = (completed.stdout + completed.stderr).strip()
    if completed.returncode:
        raise RuntimeError(output or f"planner exited with {completed.returncode}")
    return {"root": str(root), "output": output}


TOOLS = [
    {
        "name": "get_today_plan",
        "description": "Read and generate the current QA automation learning day.",
        "inputSchema": {"type": "object", "properties": {"root": {"type": "string"}}},
    },
    {
        "name": "get_progress",
        "description": "Read completed days and the next learning task.",
        "inputSchema": {"type": "object", "properties": {"root": {"type": "string"}}},
    },
    {
        "name": "create_daily_log",
        "description": "Create a daily log and evidence directory for a chosen learning day.",
        "inputSchema": {
            "type": "object",
            "properties": {"day": {"type": "integer", "minimum": 1}, "root": {"type": "string"}},
        },
    },
    {
        "name": "complete_learning_day",
        "description": "Record a completed learning day, its result, and the next step.",
        "inputSchema": {
            "type": "object",
            "required": ["day", "result"],
            "properties": {
                "day": {"type": "integer", "minimum": 1},
                "result": {"type": "string"},
                "next_step": {"type": "string"},
                "root": {"type": "string"},
            },
        },
    },
]


def tool_result(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "get_today_plan":
        return run_planner(arguments, "today")
    if name == "get_progress":
        return run_planner(arguments, "status")
    if name == "create_daily_log":
        day = arguments.get("day")
        return run_planner(arguments, "today" if day is None else "plan", *([] if day is None else [str(day)]))
    if name == "complete_learning_day":
        if "day" not in arguments or not arguments.get("result"):
            raise ValueError("complete_learning_day requires day and result")
        extra = [str(arguments["day"]), "--result", str(arguments["result"])]
        if arguments.get("next_step"):
            extra.extend(["--next-step", str(arguments["next_step"])])
        return run_planner(arguments, "complete", *extra)
    raise ValueError(f"unknown tool: {name}")


def send(message: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(message, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def handle(message: dict[str, Any]) -> None:
    method = message.get("method")
    request_id = message.get("id")
    if method == "initialize":
        requested = message.get("params", {}).get("protocolVersion", "2024-11-05")
        send({"jsonrpc": "2.0", "id": request_id, "result": {"protocolVersion": requested, "capabilities": {"tools": {}}, "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION}}})
        return
    if method == "notifications/initialized":
        return
    if method == "tools/list":
        send({"jsonrpc": "2.0", "id": request_id, "result": {"tools": TOOLS}})
        return
    if method == "tools/call":
        try:
            params = message.get("params", {})
            result = tool_result(str(params.get("name")), params.get("arguments", {}))
            send({"jsonrpc": "2.0", "id": request_id, "result": {"content": [{"type": "text", "text": result["output"]}]}})
        except Exception as exc:
            send({"jsonrpc": "2.0", "id": request_id, "result": {"isError": True, "content": [{"type": "text", "text": str(exc)}]}})
        return
    if request_id is not None:
        send({"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": f"method not found: {method}"}})


def main() -> None:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            handle(json.loads(line))
        except json.JSONDecodeError as exc:
            send({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(exc)}})


if __name__ == "__main__":
    main()
