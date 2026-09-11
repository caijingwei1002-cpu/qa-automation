"""Ensure a registered local target service is reachable before verification."""

from __future__ import annotations

import os
import subprocess
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from math import isfinite
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

LOCAL_HOSTS = {"127.0.0.1", "localhost", "::1"}
DEFAULT_HEALTH_PATH = "/ping"
DEFAULT_HEALTH_TIMEOUT_SECONDS = 1.0
DEFAULT_STARTUP_TIMEOUT_SECONDS = 30.0
DEFAULT_POLL_INTERVAL_SECONDS = 0.5


@dataclass(frozen=True)
class ServicePreflight:
    """Result of checking or starting one registered target service."""

    target_name: str
    state: str
    message: str
    pid: int | None = None

    @property
    def ok(self) -> bool:
        return self.state in {"skipped", "already-running", "started"}

    def evidence_line(self) -> str:
        """Return a safe, concise line suitable for verification evidence."""
        pid = f", pid={self.pid}" if self.pid is not None else ""
        return f"target={self.target_name}, state={self.state}{pid}, {self.message}"


def _safe_endpoint(url: str) -> str:
    """Remove credentials from an endpoint before it enters evidence."""
    try:
        parsed = urlparse(url)
        parsed_port = parsed.port
    except ValueError:
        return "<invalid-endpoint>"
    hostname = parsed.hostname or "<invalid-host>"
    if ":" in hostname and not hostname.startswith("["):
        hostname = f"[{hostname}]"
    port = f":{parsed_port}" if parsed_port else ""
    path = parsed.path or "/"
    return f"{parsed.scheme}://{hostname}{port}{path}"


def probe_health(url: str, timeout_seconds: float) -> tuple[bool, str]:
    """Probe a health endpoint without logging its body or query parameters."""
    request = Request(url, method="GET")
    try:
        with urlopen(request, timeout=timeout_seconds) as response:
            status = getattr(response, "status", None)
            if status is None:
                status = response.getcode()
            return status < 400, f"http={status}"
    except HTTPError as exc:
        return False, f"http={exc.code}"
    except (OSError, URLError, TimeoutError) as exc:
        return False, exc.__class__.__name__


def _command_from_config(raw_command: object) -> list[str] | None:
    if not isinstance(raw_command, Sequence) or isinstance(raw_command, (str, bytes)):
        return None
    command = [str(part).strip() for part in raw_command]
    if not command or any(not part for part in command):
        return None
    if os.name == "nt" and command[0].lower() == "npm":
        command[0] = "npm.cmd"
    return command


def ensure_target_service(
    target_name: str,
    definition: Mapping[str, object],
    *,
    target_root: Path,
    environ: Mapping[str, str] | None = None,
    probe: Callable[[str, float], tuple[bool, str]] = probe_health,
    popen: Callable[..., subprocess.Popen] = subprocess.Popen,
    sleep: Callable[[float], None] = time.sleep,
    monotonic: Callable[[], float] = time.monotonic,
) -> ServicePreflight:
    """Reuse a healthy local service or start the configured command on demand."""
    environment = environ if environ is not None else os.environ
    startup = definition.get("startup")
    if definition.get("kind") != "git" or not isinstance(startup, Mapping):
        return ServicePreflight(target_name, "skipped", "未配置本地自动启动命令")

    url_env = str(definition.get("url_env", "")).strip()
    base_url = environment.get(url_env) if url_env else None
    if not base_url:
        base_url = definition.get("default_url")
    if not isinstance(base_url, str) or not base_url.strip():
        return ServicePreflight(target_name, "failed", "未配置本地目标 URL")

    try:
        parsed = urlparse(base_url.strip())
        hostname = parsed.hostname
    except ValueError:
        return ServicePreflight(target_name, "failed", "目标 URL 无法解析")
    if parsed.scheme not in {"http", "https"} or hostname not in LOCAL_HOSTS:
        return ServicePreflight(
            target_name,
            "skipped",
            f"目标 {_safe_endpoint(base_url)} 不是本地地址，已跳过自动启动",
        )

    health_path = str(startup.get("health_path", DEFAULT_HEALTH_PATH)).strip()
    health_url = urljoin(base_url.rstrip("/") + "/", health_path.lstrip("/"))
    try:
        health_timeout = float(
            startup.get("health_timeout_seconds", DEFAULT_HEALTH_TIMEOUT_SECONDS)
        )
        startup_timeout = float(
            startup.get("startup_timeout_seconds", DEFAULT_STARTUP_TIMEOUT_SECONDS)
        )
        poll_interval = float(startup.get("poll_interval_seconds", DEFAULT_POLL_INTERVAL_SECONDS))
    except (TypeError, ValueError):
        return ServicePreflight(target_name, "failed", "服务启动参数必须是数字")
    if any(
        not isfinite(value) or value <= 0
        for value in (health_timeout, startup_timeout, poll_interval)
    ):
        return ServicePreflight(target_name, "failed", "服务启动参数必须为正数")

    healthy, reason = probe(health_url, health_timeout)
    if healthy:
        return ServicePreflight(
            target_name,
            "already-running",
            f"health={_safe_endpoint(health_url)}, {reason}",
        )

    command = _command_from_config(startup.get("command"))
    if command is None:
        return ServicePreflight(target_name, "failed", "startup.command 必须是非空命令数组")

    relative_directory = startup.get("working_directory", definition.get("local_directory"))
    if not isinstance(relative_directory, str) or not relative_directory.strip():
        return ServicePreflight(target_name, "failed", "未配置服务工作目录")
    working_directory = target_root / relative_directory
    if not working_directory.is_dir():
        return ServicePreflight(
            target_name,
            "failed",
            f"服务工作目录不存在：{working_directory}",
        )

    popen_kwargs: dict[str, object] = {
        "cwd": str(working_directory),
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
    }
    if os.name == "nt":
        popen_kwargs["creationflags"] = getattr(subprocess, "CREATE_NO_WINDOW", 0)

    try:
        process = popen(command, **popen_kwargs)
    except OSError as exc:
        return ServicePreflight(
            target_name,
            "failed",
            f"启动命令失败：{exc.__class__.__name__}",
        )

    deadline = monotonic() + startup_timeout
    last_reason = reason
    while True:
        healthy, last_reason = probe(health_url, health_timeout)
        if healthy:
            pid = getattr(process, "pid", None)
            return ServicePreflight(
                target_name,
                "started",
                f"health={_safe_endpoint(health_url)}, {last_reason}",
                pid=pid if isinstance(pid, int) else None,
            )

        return_code = process.poll()
        if return_code is not None:
            return ServicePreflight(
                target_name,
                "failed",
                f"进程提前退出：exit_code={return_code}, health={_safe_endpoint(health_url)}, last_probe={last_reason}",
            )

        remaining = deadline - monotonic()
        if remaining <= 0:
            break
        sleep(min(poll_interval, remaining))

    return ServicePreflight(
        target_name,
        "failed",
        f"等待服务超时：timeout={startup_timeout:g}s, health={_safe_endpoint(health_url)}, last_probe={last_reason}",
    )
