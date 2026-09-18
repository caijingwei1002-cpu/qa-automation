"""Thread-safe local bridge for the Codex App Server JSON-RPC protocol.

The browser never talks to Codex directly. This module owns one local stdio
process, persists one Codex thread per learning day, and exposes a small event
buffer that the HTTP layer can stream with Server-Sent Events.
"""

from __future__ import annotations

import glob
import json
import os
import shutil
import subprocess
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


class CodexBridgeError(RuntimeError):
    """Base bridge failure suitable for display in the workbench."""


class CodexUnavailableError(CodexBridgeError):
    """Codex executable is missing or cannot be started."""


class CodexProtocolError(CodexBridgeError):
    """The App Server rejected or failed a JSON-RPC request."""


@dataclass
class PendingCall:
    event: threading.Event = field(default_factory=threading.Event)
    response: dict[str, Any] | None = None


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def find_codex_executable() -> Path | None:
    """Find the standalone or desktop-bundled Codex executable."""
    configured = os.environ.get("CODEX_EXE")
    if configured and Path(configured).is_file():
        return Path(configured).resolve()

    candidates: list[Path] = []
    for command in ("codex.exe", "codex"):
        located = shutil.which(command)
        if located:
            candidates.append(Path(located))

    program_files = Path(os.environ.get("ProgramFiles", "C:/Program Files"))
    windows_apps_pattern = str(
        program_files / "WindowsApps" / "OpenAI.Codex_*_x64__*" / "app" / "resources" / "codex.exe"
    )
    candidates.extend(Path(value) for value in glob.glob(windows_apps_pattern))
    existing = [candidate for candidate in candidates if candidate.is_file()]
    if not existing:
        return None
    return max(existing, key=lambda value: value.stat().st_mtime_ns)


class CodexBridge:
    """Own a Codex App Server process and translate it into workbench events."""

    def __init__(
        self,
        root: Path,
        *,
        executable: Path | None = None,
        process_factory: Callable[..., subprocess.Popen[str]] = subprocess.Popen,
        request_timeout: float = 20.0,
    ) -> None:
        self.root = root.resolve()
        self.executable = executable or find_codex_executable()
        self.process_factory = process_factory
        self.request_timeout = request_timeout
        self.process: subprocess.Popen[str] | None = None
        self.initialized = False
        self.account: dict[str, Any] | None = None
        self.requires_openai_auth = True
        self.last_error: str | None = None
        self.stderr_tail: deque[str] = deque(maxlen=30)

        self._next_id = 1
        self._pending: dict[int, PendingCall] = {}
        self._pending_approvals: dict[int, dict[str, Any]] = {}
        self._events: deque[dict[str, Any]] = deque(maxlen=1500)
        self._event_seq = 0
        self._loaded_threads: set[str] = set()
        self._active_turns: dict[str, str] = {}

        self._state_lock = threading.RLock()
        self._write_lock = threading.Lock()
        self._event_condition = threading.Condition(self._state_lock)
        self._state_path = self.root / "artifacts" / "workbench-state.json"

    def status(self) -> dict[str, Any]:
        with self._state_lock:
            running = self.process is not None and self.process.poll() is None
            return {
                "available": self.executable is not None,
                "executable": str(self.executable) if self.executable else None,
                "running": running,
                "initialized": self.initialized,
                "account": self.account,
                "requires_openai_auth": self.requires_openai_auth,
                "last_error": self.last_error,
                "stderr": list(self.stderr_tail),
                "pending_approvals": [
                    {"request_id": request_id, **payload}
                    for request_id, payload in self._pending_approvals.items()
                ],
                "event_seq": self._event_seq,
            }

    def event_sequence(self) -> int:
        """Return the latest cursor for a new event-stream subscriber."""
        with self._state_lock:
            return self._event_seq

    def start(self) -> dict[str, Any]:
        with self._state_lock:
            if self.process is not None and self.process.poll() is None and self.initialized:
                return self.status()
            if self.executable is None:
                raise CodexUnavailableError(
                    "未找到 Codex CLI。请安装 Codex CLI，或设置 CODEX_EXE 后重启工作台。"
                )
            self.last_error = None
            creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
            environment = os.environ.copy()
            environment["PYTHONIOENCODING"] = "utf-8"
            try:
                self.process = self.process_factory(
                    [str(self.executable), "app-server", "--listen", "stdio://"],
                    cwd=self.root,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    bufsize=1,
                    creationflags=creation_flags,
                    env=environment,
                )
            except (OSError, subprocess.SubprocessError) as exc:
                self.last_error = str(exc)
                raise CodexUnavailableError(
                    f"Codex App Server 启动失败：{exc}。可通过 CODEX_EXE 指定独立 Codex CLI。"
                ) from exc

            threading.Thread(target=self._read_stdout, name="codex-app-server-out", daemon=True).start()
            threading.Thread(target=self._read_stderr, name="codex-app-server-err", daemon=True).start()

        try:
            self.request(
                "initialize",
                {
                    "clientInfo": {
                        "name": "qa_learning_workbench",
                        "title": "QA Learning Workbench",
                        "version": "0.2.0",
                    },
                    "capabilities": {"experimentalApi": False},
                },
            )
            self.notify("initialized", {})
            with self._state_lock:
                self.initialized = True
            account_result = self.request("account/read", {"refreshToken": False})
            with self._state_lock:
                self.account = account_result.get("account")
                self.requires_openai_auth = bool(account_result.get("requiresOpenaiAuth", True))
            self._emit("bridge/ready", self.status())
            return self.status()
        except Exception as exc:
            self.last_error = str(exc)
            self.stop()
            raise

    def stop(self) -> None:
        with self._state_lock:
            process = self.process
            self.process = None
            self.initialized = False
            pending = list(self._pending.values())
            self._pending.clear()
            self._loaded_threads.clear()
            for call in pending:
                call.response = {"error": {"message": "Codex App Server 已停止"}}
                call.event.set()
        if process is not None and process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=3)
            except (OSError, subprocess.TimeoutExpired):
                try:
                    process.kill()
                except OSError:
                    pass
        if process is not None:
            for stream in (process.stdin, process.stdout, process.stderr):
                if stream is not None:
                    try:
                        stream.close()
                    except OSError:
                        pass

    def request(self, method: str, params: dict[str, Any], *, timeout: float | None = None) -> dict[str, Any]:
        with self._state_lock:
            if self.process is None or self.process.poll() is not None:
                raise CodexUnavailableError("Codex App Server 未运行")
            request_id = self._next_id
            self._next_id += 1
            call = PendingCall()
            self._pending[request_id] = call
        self._send({"method": method, "id": request_id, "params": params})
        if not call.event.wait(timeout if timeout is not None else self.request_timeout):
            with self._state_lock:
                self._pending.pop(request_id, None)
            raise CodexProtocolError(f"Codex 请求超时：{method}")
        response = call.response or {}
        if response.get("error"):
            error = response["error"]
            message = error.get("message", str(error)) if isinstance(error, dict) else str(error)
            raise CodexProtocolError(f"{method}：{message}")
        result = response.get("result", {})
        return result if isinstance(result, dict) else {"value": result}

    def notify(self, method: str, params: dict[str, Any]) -> None:
        self._send({"method": method, "params": params})

    def _send(self, payload: dict[str, Any]) -> None:
        line = json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"
        with self._write_lock:
            process = self.process
            if process is None or process.poll() is not None or process.stdin is None:
                raise CodexUnavailableError("Codex App Server 连接已断开")
            try:
                process.stdin.write(line)
                process.stdin.flush()
            except (BrokenPipeError, OSError) as exc:
                raise CodexUnavailableError("Codex App Server 连接已断开") from exc

    def _read_stdout(self) -> None:
        process = self.process
        if process is None or process.stdout is None:
            return
        try:
            for raw_line in process.stdout:
                line = raw_line.strip()
                if not line:
                    continue
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    self.stderr_tail.append(f"非 JSON 输出：{line[:500]}")
                    continue
                self._handle_message(message)
        finally:
            return_code = process.poll()
            self.last_error = f"Codex App Server 已退出（exit {return_code}）"
            self._emit("bridge/disconnected", {"returncode": return_code, "error": self.last_error})
            with self._state_lock:
                for call in self._pending.values():
                    call.response = {"error": {"message": self.last_error}}
                    call.event.set()
                self._pending.clear()

    def _read_stderr(self) -> None:
        process = self.process
        if process is None or process.stderr is None:
            return
        for raw_line in process.stderr:
            line = raw_line.rstrip()
            if line:
                with self._state_lock:
                    self.stderr_tail.append(line[-2000:])

    def _handle_message(self, message: dict[str, Any]) -> None:
        message_id = message.get("id")
        method = message.get("method")
        if message_id is not None and not method:
            with self._state_lock:
                call = self._pending.pop(int(message_id), None)
            if call:
                call.response = message
                call.event.set()
            return
        if message_id is not None and method:
            payload = dict(message.get("params") or {})
            payload["method"] = method
            with self._state_lock:
                self._pending_approvals[int(message_id)] = payload
            self._emit(method, {"requestId": int(message_id), **payload})
            return
        if method:
            params = dict(message.get("params") or {})
            self._track_notification(method, params)
            self._emit(method, params)

    def _track_notification(self, method: str, params: dict[str, Any]) -> None:
        if method == "account/updated":
            with self._state_lock:
                self.account = {
                    **(self.account or {}),
                    "authMode": params.get("authMode"),
                    "planType": params.get("planType"),
                }
        elif method == "turn/started":
            turn = params.get("turn") or {}
            thread_id = str(params.get("threadId") or turn.get("threadId") or "")
            if thread_id and turn.get("id"):
                with self._state_lock:
                    self._active_turns[thread_id] = str(turn["id"])
        elif method == "turn/completed":
            turn = params.get("turn") or {}
            thread_id = str(params.get("threadId") or turn.get("threadId") or "")
            if thread_id:
                with self._state_lock:
                    self._active_turns.pop(thread_id, None)
        elif method == "serverRequest/resolved":
            request_id = params.get("requestId")
            if request_id is not None:
                with self._state_lock:
                    self._pending_approvals.pop(int(request_id), None)

    def _emit(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        with self._event_condition:
            self._event_seq += 1
            event = {
                "seq": self._event_seq,
                "time": utc_now(),
                "method": method,
                "params": params,
            }
            self._events.append(event)
            self._event_condition.notify_all()
            return event

    def events_after(self, sequence: int, *, timeout: float = 15.0) -> list[dict[str, Any]]:
        deadline = time.monotonic() + timeout
        with self._event_condition:
            while self._event_seq <= sequence and time.monotonic() < deadline:
                self._event_condition.wait(max(0.0, deadline - time.monotonic()))
            return [event for event in self._events if int(event["seq"]) > sequence]

    def login_with_chatgpt(self) -> dict[str, Any]:
        self._ensure_started()
        return self.request(
            "account/login/start",
            {"type": "chatgpt", "useHostedLoginSuccessPage": True, "appBrand": "chatgpt"},
        )

    def thread_id_for_day(self, day: int) -> str | None:
        state = self._load_state()
        record = state.get("days", {}).get(str(day), {})
        thread_id = record.get("thread_id") if isinstance(record, dict) else None
        return str(thread_id) if thread_id else None

    @staticmethod
    def _is_missing_rollout_error(error: CodexProtocolError) -> bool:
        """Return whether App Server has permanently lost a saved thread."""
        return "no rollout found for thread id" in str(error).lower()

    def _start_learning_thread(self) -> tuple[str, dict[str, Any]]:
        result = self.request(
            "thread/start",
            {
                "cwd": str(self.root),
                "approvalPolicy": "on-request",
                "sandbox": "workspace-write",
                "personality": "friendly",
                "serviceName": "qa_learning_workbench",
            },
        )
        thread = result.get("thread") or {}
        thread_id = thread.get("id")
        if not thread_id:
            raise CodexProtocolError("thread/start 未返回 thread.id")
        return str(thread_id), thread

    def session_for_day(self, day: int, plan: dict[str, Any], *, bootstrap: bool = True) -> dict[str, Any]:
        self._ensure_started()
        state = self._load_state()
        day_key = str(day)
        record = dict(state.get("days", {}).get(day_key, {}))
        created = False
        thread_snapshot: dict[str, Any] | None = None
        thread_id = record.get("thread_id")
        replaced_thread_id: str | None = None
        if thread_id:
            thread_id = str(thread_id)
            if thread_id not in self._loaded_threads:
                try:
                    self.request("thread/resume", {"threadId": thread_id, "personality": "friendly"})
                except CodexProtocolError as error:
                    if not self._is_missing_rollout_error(error):
                        raise
                    replaced_thread_id = thread_id
                    thread_id = None
                else:
                    self._loaded_threads.add(thread_id)
        if not thread_id:
            thread_id, thread_snapshot = self._start_learning_thread()
            record = {"thread_id": thread_id, "created_at": utc_now(), "bootstrapped": False}
            if replaced_thread_id:
                record["replaced_thread_id"] = replaced_thread_id
            state.setdefault("days", {})[day_key] = record
            self._save_state(state)
            self._loaded_threads.add(thread_id)
            created = True

        bootstrapped_now = False
        if bootstrap and not record.get("bootstrapped"):
            self.start_turn(thread_id, self._learning_bootstrap(day, plan))
            record["bootstrapped"] = True
            bootstrapped_now = True
            state.setdefault("days", {})[day_key] = record
            self._save_state(state)
        if record.get("bootstrapped") and not created and not bootstrapped_now:
            history_result = self.request("thread/read", {"threadId": thread_id, "includeTurns": True})
            thread_snapshot = history_result.get("thread", history_result)
        if thread_snapshot is None:
            # A newly started thread is not materialized until its first user
            # message. Return the start snapshot and let streamed events fill in
            # the bootstrap turn instead of reading full history too early.
            thread_snapshot = {"id": thread_id, "turns": []}
        return {
            "day": day,
            "thread_id": thread_id,
            "created": created,
            "thread": thread_snapshot,
            "active_turn_id": self._active_turns.get(str(thread_id)),
        }

    def start_turn(self, thread_id: str, text: str) -> dict[str, Any]:
        self._ensure_started()
        cleaned = text.strip()
        if not cleaned:
            raise CodexProtocolError("消息不能为空")
        result = self.request(
            "turn/start",
            {
                "threadId": thread_id,
                "input": [{"type": "text", "text": cleaned}],
                "cwd": str(self.root),
                "approvalPolicy": "on-request",
                "sandboxPolicy": {
                    "type": "workspaceWrite",
                    "writableRoots": [str(self.root)],
                    "networkAccess": False,
                },
                "personality": "friendly",
                "summary": "concise",
            },
        )
        turn = result.get("turn") or {}
        if turn.get("id"):
            with self._state_lock:
                self._active_turns[thread_id] = str(turn["id"])
        return result

    def interrupt(self, thread_id: str, turn_id: str | None = None) -> dict[str, Any]:
        active_turn = turn_id or self._active_turns.get(thread_id)
        if not active_turn:
            raise CodexProtocolError("当前没有正在运行的 Codex 回合")
        return self.request("turn/interrupt", {"threadId": thread_id, "turnId": active_turn})

    def resolve_approval(self, request_id: int, decision: str) -> dict[str, Any]:
        allowed = {"accept", "acceptForSession", "decline", "cancel"}
        if decision not in allowed:
            raise CodexProtocolError("无效的审批决定")
        with self._state_lock:
            approval = self._pending_approvals.get(request_id)
            if approval is None:
                raise CodexProtocolError("审批请求已失效或不存在")
        if approval.get("method") == "item/permissions/requestApproval":
            requested = approval.get("permissions") or approval.get("requestedPermissions") or {}
            result = {
                "permissions": requested if decision.startswith("accept") else {},
                "scope": "session" if decision == "acceptForSession" else "turn",
            }
        else:
            result = {"decision": decision}
        self._send({"id": int(request_id), "result": result})
        with self._state_lock:
            self._pending_approvals.pop(int(request_id), None)
        return {"request_id": int(request_id), "decision": decision}

    def _ensure_started(self) -> None:
        if self.process is None or self.process.poll() is not None or not self.initialized:
            self.start()

    def _load_state(self) -> dict[str, Any]:
        if not self._state_path.exists():
            return {"version": 1, "days": {}}
        try:
            value = json.loads(self._state_path.read_text(encoding="utf-8"))
            return value if isinstance(value, dict) else {"version": 1, "days": {}}
        except (OSError, json.JSONDecodeError):
            return {"version": 1, "days": {}}

    def _save_state(self, value: dict[str, Any]) -> None:
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self._state_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, self._state_path)

    def _learning_bootstrap(self, day: int, plan: dict[str, Any]) -> str:
        timebox = plan.get("timebox") or {}
        return f"""你是我的 QA 自动化学习教练。我们现在开始 Day {day} 的学习，不要一次性直接给出完整答案。

今日主题：{plan.get('title') or plan.get('theme')}
核心知识：{plan.get('learn')}
实践任务：{plan.get('deliverable') or plan.get('task')}
目标文件：{plan.get('file')}
验证命令：{plan.get('run')}
完成标准：{plan.get('done')}
知识检查：{plan.get('knowledge_check')}
时间盒：复习、讨论与设计 {timebox.get('study_minutes', 30)} 分钟，实践 {timebox.get('practice_minutes', 40)} 分钟，验证 {timebox.get('verification_minutes', 25)} 分钟，审查迁移 {timebox.get('review_minutes', 25)} 分钟，复盘 {timebox.get('reflection_minutes', 15)} 分钟。

请遵循以下教学方式：
1. 先读 AGENTS.md 和 docs/INTERACTIVE-LEARNING.md，运行 plan_day.py check-day {day} 和 session {day}。
2. 按 config/learning-workflow.json 七步顺序，从未完成步骤继续；不要把续学重置为第一步。
3. 让我先讨论需求、设计和编码；真实记录提示程度，协助实现不能算独立完成。
4. 用 checkpoint 保存实际进展，卡点保存为 in_progress；步骤导航不代表完成。
5. 使用统一验证入口；先根据失败证据分析，再修复和回归。
6. 审查、修改、复审后给未提供答案的迁移题，等待我实际作答，不能自问自答。
7. 我明确确认完成后，先知识日志落盘，再用 complete 校验并推进；不要直接修改 progress.json。

现在先核对进度和续学位置，然后只布置当前步骤的一个问题或动作。"""
