#!/usr/bin/env python3
"""Local-first QA Automation Learning Workbench.

The server intentionally uses only the Python standard library. It exposes a
small, localhost-only API over the existing JSON/Markdown/Git repository and
never offers an arbitrary shell endpoint.
"""

from __future__ import annotations

import argparse
import difflib
import glob
import importlib.util
import json
import mimetypes
import os
import shlex
import shutil
import subprocess
import sys
import threading
import time
import uuid
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from codex_bridge import CodexBridge, CodexBridgeError, CodexUnavailableError

MAX_FILE_BYTES = 2 * 1024 * 1024
TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".txt",
    ".ps1",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".html",
    ".css",
    ".xml",
    ".feature",
}
IGNORED_DIRECTORIES = {
    ".git",
    ".idea",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "playwright-report",
    "test-results",
}
ROOT_READABLE_FILES = {
    "README.md",
    "ROADMAP.md",
    "LEARNING-NOTES.md",
    "progress.json",
    "curriculum.json",
    "daily-plan.json",
}
WRITABLE_ROOTS = ("test-projects", "daily-log")
WRITABLE_FILES = {"LEARNING-NOTES.md"}
PLANNER_CACHE: dict[str, Any] = {}


class WorkbenchError(Exception):
    def __init__(self, message: str, status: int = HTTPStatus.BAD_REQUEST):
        super().__init__(message)
        self.status = int(status)


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def normalize_relative_path(value: str) -> Path:
    normalized = value.strip().replace("\\", "/")
    if not normalized:
        raise WorkbenchError("文件路径不能为空")
    candidate = Path(normalized)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise WorkbenchError("文件路径超出工作区")
    return candidate


def resolve_project_path(root: Path, value: str, *, write: bool = False) -> Path:
    relative = normalize_relative_path(value)
    resolved_root = root.resolve()
    resolved = (resolved_root / relative).resolve()
    if not is_within(resolved, resolved_root):
        raise WorkbenchError("文件路径超出工作区")

    relative_posix = relative.as_posix()
    readable = (
        relative.parts[0] in {"test-projects", "daily-log", "artifacts", "config"}
        or relative_posix in ROOT_READABLE_FILES
    )
    if not readable:
        raise WorkbenchError("该文件不在工作台允许访问的范围内", HTTPStatus.FORBIDDEN)

    if write:
        writable = relative.parts[0] in WRITABLE_ROOTS or relative_posix in WRITABLE_FILES
        if not writable:
            raise WorkbenchError("该文件为只读资源", HTTPStatus.FORBIDDEN)
        if resolved.suffix.lower() not in TEXT_SUFFIXES:
            raise WorkbenchError("工作台只允许保存文本代码和学习文档", HTTPStatus.FORBIDDEN)
    return resolved


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_planner(root: Path) -> Any:
    cache_key = str(root.resolve())
    if cache_key in PLANNER_CACHE:
        return PLANNER_CACHE[cache_key]
    planner_path = root / "tools" / "plan_day.py"
    if not planner_path.is_file():
        raise WorkbenchError(f"未找到学习计划工具：{planner_path}", HTTPStatus.NOT_FOUND)
    tools_path = str(planner_path.parent)
    if tools_path not in sys.path:
        sys.path.insert(0, tools_path)
    module_name = f"qa_workbench_plan_day_{abs(hash(cache_key))}"
    spec = importlib.util.spec_from_file_location(module_name, planner_path)
    if spec is None or spec.loader is None:
        raise WorkbenchError("无法加载学习计划工具", HTTPStatus.INTERNAL_SERVER_ERROR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    PLANNER_CACHE[cache_key] = module
    return module


def git_status(root: Path) -> list[dict[str, str]]:
    completed = subprocess.run(
        ["git", "status", "--short"],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    entries: list[dict[str, str]] = []
    for line in completed.stdout.splitlines():
        if len(line) < 4:
            continue
        status = line[:2].strip() or line[:2]
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        entries.append({"status": status, "path": path.replace("\\", "/")})
    return entries


def phase_progress(
    curriculum: dict[str, Any], completed_days: set[int], current_day: int
) -> list[dict[str, Any]]:
    phases: list[dict[str, Any]] = []
    start = 1
    for phase in curriculum.get("phases", []):
        total = int(phase.get("days", 0))
        end = start + total - 1
        completed = sum(1 for day in completed_days if start <= day <= end)
        phases.append(
            {
                "id": phase.get("id"),
                "name": phase.get("name"),
                "objective": phase.get("objective"),
                "project": phase.get("project"),
                "start_day": start,
                "end_day": end,
                "completed": completed,
                "total": total,
                "percent": round((completed / total * 100) if total else 0, 1),
                "active": start <= current_day <= end,
            }
        )
        start = end + 1
    return phases


def evidence_files(root: Path, day: int) -> list[dict[str, Any]]:
    evidence_root = root / "artifacts" / f"day-{day:03d}"
    if not evidence_root.exists():
        return []
    files: list[dict[str, Any]] = []
    for path in sorted(evidence_root.rglob("*")):
        if path.is_file():
            files.append(
                {
                    "path": path.relative_to(root).as_posix(),
                    "name": path.name,
                    "size": path.stat().st_size,
                }
            )
    return files[:100]


def build_dashboard(root: Path) -> dict[str, Any]:
    planner = load_planner(root)
    curriculum = load_json(root / "curriculum.json", {})
    progress = planner.load_progress()
    current_day = int(progress.get("current_day", 1))
    completed_days = {int(day) for day in progress.get("completed_days", [])}
    plan = planner.plan_for_day(curriculum, current_day)
    core_days = int(curriculum.get("core_days", 0))
    phases = phase_progress(curriculum, completed_days, current_day)
    active_phase = next((phase for phase in phases if phase["active"]), None)
    status_entries = git_status(root)
    current_project = str(plan.get("test_project", plan.get("project", "")))
    relevant_changes = [
        entry
        for entry in status_entries
        if entry["path"].startswith(current_project.rstrip("/") + "/")
    ]
    log_path = root / "daily-log" / f"day-{current_day:03d}.md"
    notes_path = root / "LEARNING-NOTES.md"
    notes_heading = f"## Day {current_day}：{plan.get('title') or plan.get('theme')}"
    notes_written = notes_path.exists() and notes_heading in notes_path.read_text(encoding="utf-8")
    return {
        "root": str(root),
        "progress": {
            "current_day": current_day,
            "completed": len(completed_days),
            "core_days": core_days,
            "percent": (
                None
                if curriculum.get("planning_mode") == "rolling"
                else round((len(completed_days) / core_days * 100) if core_days else 0, 1)
            ),
            "detailed_horizon_percent": round(
                (len(completed_days) / core_days * 100) if core_days else 0, 1
            ),
            "planning_mode": curriculum.get("planning_mode", "fixed"),
            "scope_label": (
                f"已完成 {len(completed_days)} 天 · 当前细化至 Day {core_days}"
                if curriculum.get("planning_mode") == "rolling"
                else f"{len(completed_days)} / {core_days} 天"
            ),
        },
        "active_phase": active_phase,
        "phases": phases,
        "plan": plan,
        "learning_session": planner.session_summary(root, current_day),
        "history": list(progress.get("history", []))[-6:][::-1],
        "workspace": {
            "log_exists": log_path.exists(),
            "log_path": log_path.relative_to(root).as_posix(),
            "notes_written": notes_written,
            "changes": relevant_changes,
            "evidence": evidence_files(root, current_day),
        },
    }


def list_workspace_files(root: Path, project: str | None = None) -> dict[str, Any]:
    base_relative = project or "test-projects"
    base = resolve_project_path(root, base_relative)
    if not base.is_dir():
        raise WorkbenchError("当前项目目录不存在", HTTPStatus.NOT_FOUND)
    files: list[dict[str, Any]] = []
    for path in sorted(base.rglob("*")):
        if any(part in IGNORED_DIRECTORIES for part in path.relative_to(base).parts):
            continue
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        stat = path.stat()
        files.append(
            {
                "path": path.relative_to(root).as_posix(),
                "name": path.name,
                "size": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
            }
        )
        if len(files) >= 2000:
            break
    return {"base": base.relative_to(root).as_posix(), "files": files}


def read_text_file(root: Path, relative_path: str) -> dict[str, Any]:
    path = resolve_project_path(root, relative_path)
    if not path.is_file():
        raise WorkbenchError("文件不存在", HTTPStatus.NOT_FOUND)
    stat = path.stat()
    if stat.st_size > MAX_FILE_BYTES:
        raise WorkbenchError("文件超过 2 MB，工作台只提供预览", HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
    if path.suffix.lower() not in TEXT_SUFFIXES:
        raise WorkbenchError("该文件不是可编辑文本", HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    return {
        "path": path.relative_to(root).as_posix(),
        "content": path.read_bytes().decode("utf-8", errors="replace"),
        "mtime_ns": stat.st_mtime_ns,
        "writable": is_writable_relative(path.relative_to(root)),
        "language": language_for(path),
    }


def is_writable_relative(relative: Path) -> bool:
    return relative.as_posix() in WRITABLE_FILES or relative.parts[0] in WRITABLE_ROOTS


def language_for(path: Path) -> str:
    return {
        ".py": "Python",
        ".md": "Markdown",
        ".json": "JSON",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript React",
        ".html": "HTML",
        ".css": "CSS",
        ".ps1": "PowerShell",
    }.get(path.suffix.lower(), "Text")


def save_text_file(
    root: Path, relative_path: str, content: str, expected_mtime_ns: int
) -> dict[str, Any]:
    path = resolve_project_path(root, relative_path, write=True)
    if not path.is_file():
        raise WorkbenchError("第一版工作台只编辑已有文件", HTTPStatus.NOT_FOUND)
    current_stat = path.stat()
    if current_stat.st_mtime_ns != int(expected_mtime_ns):
        raise WorkbenchError(
            "文件已被 PyCharm 或其他程序修改，请重新加载后再保存", HTTPStatus.CONFLICT
        )
    original_bytes = path.read_bytes()
    newline = "\r\n" if b"\r\n" in original_bytes else "\n"
    normalized_content = content.replace("\r\n", "\n").replace("\r", "\n")
    encoded_content = normalized_content.replace("\n", newline).encode("utf-8")
    if len(encoded_content) > MAX_FILE_BYTES:
        raise WorkbenchError("保存内容超过 2 MB", HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
    temporary = path.with_name(f".{path.name}.workbench-{uuid.uuid4().hex}.tmp")
    try:
        temporary.write_bytes(encoded_content)
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()
    stat = path.stat()
    return {
        "path": path.relative_to(root).as_posix(),
        "mtime_ns": stat.st_mtime_ns,
        "size": stat.st_size,
    }


def file_diff(root: Path, relative_path: str) -> dict[str, Any]:
    path = resolve_project_path(root, relative_path)
    relative = path.relative_to(root).as_posix()
    status_entry = next((item for item in git_status(root) if item["path"] == relative), None)
    if status_entry and status_entry["status"] == "??":
        content = path.read_text(encoding="utf-8", errors="replace").splitlines()
        diff = "\n".join(
            difflib.unified_diff(
                [], content, fromfile="/dev/null", tofile=f"b/{relative}", lineterm=""
            )
        )
    else:
        completed = subprocess.run(
            ["git", "diff", "HEAD", "--", relative],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        diff = completed.stdout or completed.stderr
    return {
        "path": relative,
        "status": status_entry["status"] if status_entry else "clean",
        "diff": diff,
    }


def parse_allowed_pytest(command: str) -> list[str]:
    if any(character in command for character in (";", "|", "&", ">", "<", "`")):
        raise WorkbenchError("计划命令包含工作台不允许的 Shell 操作", HTTPStatus.FORBIDDEN)
    tokens = shlex.split(command, posix=False)
    if not tokens or tokens[0].lower() not in {"pytest", "pytest.exe"}:
        raise WorkbenchError(
            "第一版工作台只允许运行计划中的 pytest 命令", HTTPStatus.NOT_IMPLEMENTED
        )
    return tokens[1:]


def run_current_tests(root: Path) -> dict[str, Any]:
    planner = load_planner(root)
    curriculum = load_json(root / "curriculum.json", {})
    progress = planner.load_progress()
    day = int(progress.get("current_day", 1))
    plan = planner.plan_for_day(curriculum, day)
    command = str(plan.get("run", "")).strip()
    parse_allowed_pytest(command)
    parse_allowed_pytest(plan["full_run"])
    record = planner.execute_verification(day)
    returncode = next(
        (record[k]["exit_code"] for k in ("target", "regression") if record[k]["exit_code"] != 0), 0
    )
    output = record["target"]["output"] + "\n" + record["regression"]["output"]
    return {
        "day": day,
        "command": command,
        "returncode": returncode,
        "passed": returncode == 0,
        "duration_seconds": record["duration_seconds"],
        "output": output[-200_000:],
        "evidence": f"artifacts/day-{day:03d}/verification.md",
    }


def run_validation(root: Path) -> dict[str, Any]:
    python = root / ".venv" / "Scripts" / "python.exe"
    executable = str(python if python.exists() else Path(sys.executable))
    commands = [
        (["git", "diff", "--check"], "git diff --check"),
        ([executable, "tools/validate_repo.py"], "validate_repo.py"),
    ]
    results: list[dict[str, Any]] = []
    for argv, label in commands:
        completed = subprocess.run(
            argv,
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        results.append(
            {
                "name": label,
                "returncode": completed.returncode,
                "passed": completed.returncode == 0,
                "output": (completed.stdout + completed.stderr).strip(),
            }
        )
    return {"passed": all(result["passed"] for result in results), "results": results}


def find_pycharm() -> Path | None:
    configured = os.environ.get("PYCHARM_EXE")
    if configured and Path(configured).is_file():
        return Path(configured)
    for command in ("pycharm64.exe", "pycharm.exe", "pycharm64", "pycharm"):
        located = shutil.which(command)
        if located:
            return Path(located)
    patterns = [
        str(
            Path(os.environ.get("ProgramFiles", "C:/Program Files"))
            / "JetBrains"
            / "PyCharm*"
            / "bin"
            / "pycharm64.exe"
        ),
        str(
            Path(os.environ.get("LOCALAPPDATA", ""))
            / "Programs"
            / "PyCharm*"
            / "bin"
            / "pycharm64.exe"
        ),
        str(
            Path(os.environ.get("LOCALAPPDATA", ""))
            / "JetBrains"
            / "Toolbox"
            / "apps"
            / "PyCharm*"
            / "*"
            / "*"
            / "bin"
            / "pycharm64.exe"
        ),
    ]
    candidates: list[Path] = []
    for pattern in patterns:
        candidates.extend(Path(candidate) for candidate in glob.glob(pattern))
    existing = [candidate for candidate in candidates if candidate.is_file()]
    return max(existing, key=lambda item: item.stat().st_mtime_ns) if existing else None


def open_in_pycharm(root: Path, relative_path: str | None, line: int = 1) -> dict[str, Any]:
    executable = find_pycharm()
    if executable is None:
        raise WorkbenchError(
            "未找到 PyCharm。请设置 PYCHARM_EXE 环境变量后重启工作台。", HTTPStatus.NOT_FOUND
        )
    if relative_path:
        path = resolve_project_path(root, relative_path)
        arguments = [str(executable), "--line", str(max(1, int(line))), str(path)]
    else:
        arguments = [str(executable), str(root)]
    subprocess.Popen(
        arguments,
        cwd=root,
        creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
    )
    return {"opened": relative_path or str(root), "executable": str(executable)}


class WorkbenchServer(ThreadingHTTPServer):
    project_root: Path
    static_root: Path
    codex: CodexBridge


class WorkbenchHandler(BaseHTTPRequestHandler):
    server: WorkbenchServer

    def log_message(self, format: str, *args: Any) -> None:
        sys.stdout.write(f"[{self.log_date_time_string()}] {format % args}\n")

    def send_json(self, payload: Any, status: int = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(int(status))
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, error: Exception) -> None:
        if isinstance(error, WorkbenchError):
            status = error.status
        elif isinstance(error, CodexUnavailableError):
            status = HTTPStatus.SERVICE_UNAVAILABLE
        elif isinstance(error, CodexBridgeError):
            status = HTTPStatus.BAD_GATEWAY
        else:
            status = HTTPStatus.INTERNAL_SERVER_ERROR
        self.send_json({"error": str(error)}, status)

    def read_json_body(self) -> dict[str, Any]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise WorkbenchError("无效的请求长度") from exc
        if length <= 0 or length > MAX_FILE_BYTES + 65_536:
            raise WorkbenchError("请求体为空或过大", HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
        try:
            value = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise WorkbenchError("请求体不是有效 JSON") from exc
        if not isinstance(value, dict):
            raise WorkbenchError("请求体必须是 JSON 对象")
        return value

    def do_GET(self) -> None:
        try:
            parsed = urlparse(self.path)
            query = parse_qs(parsed.query)
            if parsed.path == "/api/dashboard":
                self.send_json(build_dashboard(self.server.project_root))
                return
            if parsed.path == "/api/tree":
                project = query.get("project", [None])[0]
                self.send_json(list_workspace_files(self.server.project_root, project))
                return
            if parsed.path == "/api/file":
                relative = query.get("path", [""])[0]
                self.send_json(read_text_file(self.server.project_root, relative))
                return
            if parsed.path == "/api/diff":
                relative = query.get("path", [""])[0]
                self.send_json(file_diff(self.server.project_root, relative))
                return
            if parsed.path == "/api/chat/status":
                self.send_json(self.server.codex.status())
                return
            if parsed.path == "/api/chat/events/poll":
                self.poll_codex_events(query)
                return
            if parsed.path == "/api/chat/events":
                self.stream_codex_events()
                return
            self.serve_static(parsed.path)
        except Exception as exc:
            self.send_error_json(exc)

    def do_PUT(self) -> None:
        try:
            if urlparse(self.path).path != "/api/file":
                raise WorkbenchError("未找到接口", HTTPStatus.NOT_FOUND)
            body = self.read_json_body()
            result = save_text_file(
                self.server.project_root,
                str(body.get("path", "")),
                str(body.get("content", "")),
                int(body.get("mtime_ns", 0)),
            )
            self.send_json(result)
        except Exception as exc:
            self.send_error_json(exc)

    def do_POST(self) -> None:
        try:
            route = urlparse(self.path).path
            if route == "/api/run-current":
                self.send_json(run_current_tests(self.server.project_root))
                return
            if route == "/api/validate":
                self.send_json(run_validation(self.server.project_root))
                return
            if route == "/api/open-pycharm":
                body = self.read_json_body()
                relative = body.get("path")
                self.send_json(
                    open_in_pycharm(
                        self.server.project_root,
                        str(relative) if relative else None,
                        int(body.get("line", 1)),
                    )
                )
                return
            if route == "/api/chat/connect":
                self.send_json(self.server.codex.start())
                return
            if route == "/api/chat/login":
                self.send_json(self.server.codex.login_with_chatgpt())
                return
            if route == "/api/chat/session":
                dashboard = build_dashboard(self.server.project_root)
                day = int(dashboard["progress"]["current_day"])
                self.send_json(
                    self.server.codex.session_for_day(day, dashboard["plan"], bootstrap=True)
                )
                return
            if route == "/api/chat/message":
                body = self.read_json_body()
                dashboard = build_dashboard(self.server.project_root)
                day = int(dashboard["progress"]["current_day"])
                thread_id = self.server.codex.thread_id_for_day(day)
                if not thread_id or str(body.get("thread_id", "")) != thread_id:
                    raise WorkbenchError("当前学习会话已变化，请刷新页面", HTTPStatus.CONFLICT)
                self.send_json(self.server.codex.start_turn(thread_id, str(body.get("text", ""))))
                return
            if route == "/api/chat/interrupt":
                body = self.read_json_body()
                dashboard = build_dashboard(self.server.project_root)
                day = int(dashboard["progress"]["current_day"])
                thread_id = self.server.codex.thread_id_for_day(day)
                if not thread_id or str(body.get("thread_id", "")) != thread_id:
                    raise WorkbenchError("当前学习会话已变化，请刷新页面", HTTPStatus.CONFLICT)
                turn_id = str(body.get("turn_id")) if body.get("turn_id") else None
                self.send_json(self.server.codex.interrupt(thread_id, turn_id))
                return
            if route == "/api/chat/approval":
                body = self.read_json_body()
                self.send_json(
                    self.server.codex.resolve_approval(
                        int(body.get("request_id", 0)),
                        str(body.get("decision", "")),
                    )
                )
                return
            raise WorkbenchError("未找到接口", HTTPStatus.NOT_FOUND)
        except Exception as exc:
            self.send_error_json(exc)

    def stream_codex_events(self) -> None:
        try:
            last_event_id = self.headers.get("Last-Event-ID")
            requested_cursor = parse_qs(urlparse(self.path).query).get("after", [None])[0]
            if last_event_id is not None:
                sequence = int(last_event_id or 0)
            elif requested_cursor is not None:
                sequence = int(requested_cursor or 0)
            else:
                sequence = self.server.codex.event_sequence()
        except ValueError:
            sequence = self.server.codex.event_sequence()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        deadline = time.monotonic() + 45
        try:
            initial = json.dumps(
                {"seq": sequence, "method": "bridge/status", "params": self.server.codex.status()},
                ensure_ascii=False,
            )
            self.wfile.write(f"event: codex\ndata: {initial}\n\n".encode("utf-8"))
            self.wfile.flush()
            while time.monotonic() < deadline:
                events = self.server.codex.events_after(sequence, timeout=10)
                if not events:
                    self.wfile.write(b": keep-alive\n\n")
                    self.wfile.flush()
                    continue
                for event in events:
                    sequence = int(event["seq"])
                    payload = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
                    self.wfile.write(
                        f"id: {sequence}\nevent: codex\ndata: {payload}\n\n".encode("utf-8")
                    )
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            return

    def poll_codex_events(self, query: dict[str, list[str]]) -> None:
        """Return the next event batch using a resumable cursor.

        Long polling is intentionally available alongside SSE because the Codex
        desktop webview can suspend a streaming response while a local request is
        in flight. The cursor keeps reconnects lossless and de-duplicates events.
        """
        try:
            sequence = int(query.get("after", ["0"])[0] or 0)
        except ValueError as exc:
            raise WorkbenchError("事件游标无效") from exc
        events = self.server.codex.events_after(sequence, timeout=10)
        cursor = int(events[-1]["seq"]) if events else sequence
        self.send_json({"events": events, "cursor": cursor})

    def serve_static(self, request_path: str) -> None:
        relative = "index.html" if request_path in {"", "/"} else unquote(request_path).lstrip("/")
        if relative.startswith("static/"):
            relative = relative.removeprefix("static/")
        path = (self.server.static_root / relative).resolve()
        if not is_within(path, self.server.static_root.resolve()) or not path.is_file():
            raise WorkbenchError("页面不存在", HTTPStatus.NOT_FOUND)
        body = path.read_bytes()
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header(
            "Content-Type", f"{mime}; charset=utf-8" if mime.startswith("text/") else mime
        )
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, help="qa-automation-learning 仓库路径")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--open", action="store_true", help="启动后打开浏览器")
    parser.add_argument("--allow-remote", action="store_true", help="显式允许监听非本机地址")
    parser.add_argument("--codex-exe", type=Path, help="Codex CLI 可执行文件路径")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configured_root = (
        Path(os.environ["QA_LEARNING_ROOT"]) if os.environ.get("QA_LEARNING_ROOT") else None
    )
    root = (args.root or configured_root or Path(__file__).resolve().parents[1]).resolve()
    if not (root / "progress.json").is_file() or not (root / "daily-plan.json").is_file():
        raise SystemExit(f"不是有效的 qa-automation-learning 仓库：{root}")
    if args.host not in {"127.0.0.1", "localhost", "::1"} and not args.allow_remote:
        raise SystemExit("为保护本地代码，默认只允许监听本机地址；远程监听需要 --allow-remote")
    server = WorkbenchServer((args.host, args.port), WorkbenchHandler)
    server.project_root = root
    server.static_root = Path(__file__).resolve().parent / "static"
    server.codex = CodexBridge(root, executable=args.codex_exe)
    url = f"http://{args.host}:{args.port}"
    print(f"QA Learning Workbench: {url}")
    print(f"Repository: {root}")
    if args.open:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nWorkbench stopped.")
    finally:
        server.codex.stop()
        server.server_close()


if __name__ == "__main__":
    main()
