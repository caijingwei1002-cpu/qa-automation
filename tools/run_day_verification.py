#!/usr/bin/env python3
"""Run the daily checks and write the standard verification.md evidence."""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from learning_workflow import atomic_json, project_fingerprint  # noqa: E402
from plan_day import (  # noqa: E402
    CURRICULUM_PATH,
    default_full_run,
    load_json,
    plan_for_day,
    render_verification,
    verification_path,
)
from target_service import ServicePreflight, ensure_target_service  # noqa: E402

SENSITIVE_VALUE = re.compile(
    r"""(?i)(["']?(?:token|password|authorization|cookie)["']?\s*[:=]\s*["']?)([^"'\s,;}]+)"""
)
TARGETS_PATH = ROOT / "config" / "targets.json"


def project_python() -> Path:
    """优先使用仓库虚拟环境，避免误调用系统 Python。"""
    candidates = (
        ROOT / ".venv" / "Scripts" / "python.exe",
        ROOT / ".venv" / "bin" / "python",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return Path(sys.executable)


def display_python_path(python_path: Path) -> str:
    """生成适合写入证据的解释器路径。"""
    try:
        relative = python_path.relative_to(ROOT)
    except ValueError:
        return str(python_path)
    return ".\\" + str(relative).replace("/", "\\")


def prepare_command(command: str, python_path: Path) -> tuple[list[str], str]:
    """把 pytest 命令绑定到仓库虚拟环境，并返回实际命令和展示命令。"""
    parts = shlex.split(command)
    if not parts:
        raise ValueError("daily run command is empty")

    first = Path(parts[0]).name.lower()
    python_label = display_python_path(python_path)
    if first in {"pytest", "pytest.exe"}:
        actual = [str(python_path), "-m", "pytest", *parts[1:]]
        display = [python_label, "-m", "pytest", *parts[1:]]
        return actual, subprocess.list2cmdline(display)

    if (
        first in {"python", "python.exe", "python3"}
        and len(parts) >= 3
        and parts[1] == "-m"
        and parts[2].lower() == "pytest"
    ):
        actual = [str(python_path), "-m", "pytest", *parts[3:]]
        display = [python_label, "-m", "pytest", *parts[3:]]
        return actual, subprocess.list2cmdline(display)

    return parts, subprocess.list2cmdline(parts)


def redact_output(output: str) -> str:
    """对测试输出中的常见敏感字段做最小脱敏。"""
    return SENSITIVE_VALUE.sub(r"\1<redacted>", output)


def existing_notes(path: Path, heading: str) -> str | None:
    """读取已有的人工验证说明，避免重复运行时覆盖学习者补充的内容。"""
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    start = text.find(heading)
    if start == -1:
        return None
    next_heading = re.search(r"\n## ", text[start + len(heading) :])
    end = start + len(heading) + next_heading.start() if next_heading else len(text)
    body = text[start + len(heading) : end].strip()
    if not body or any(marker in body for marker in ("待补充", "待记录", "待填写")):
        return None
    return body


def run_command(actual: list[str], display: str, timeout: float = 300) -> tuple[str, int]:
    """执行命令并生成可写入证据的结果文本。"""
    try:
        completed = subprocess.run(
            actual,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            check=False,
        )
        output = "\n".join(
            part for part in (completed.stdout.strip(), completed.stderr.strip()) if part
        )
        output = redact_output(output) or "<no output>"
        status = "passed" if completed.returncode == 0 else "failed"
        return f"exit_code={completed.returncode} ({status})\n{output}", completed.returncode
    except subprocess.TimeoutExpired as exc:

        def decode(value: str | bytes | None) -> str:
            return (
                value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value or ""
            )

        output = redact_output(decode(exc.stdout) + decode(exc.stderr))
        return f"exit_code=124 (failed)\ntimeout={timeout}s\n{output}", 124
    except OSError as exc:
        return (
            f"exit_code=127 (failed)\ncommand={display}\nerror={exc.__class__.__name__}: {exc}",
            127,
        )


def target_for_plan(plan: dict[str, object]) -> tuple[str, dict[str, object]] | None:
    """Find the registered target associated with a daily test project."""
    project = str(plan.get("test_project", plan.get("project", ""))).rstrip("/")
    registry = load_json(TARGETS_PATH, {})
    targets = registry.get("targets", {}) if isinstance(registry, dict) else {}
    if not isinstance(targets, dict):
        return None
    for name, definition in targets.items():
        if not isinstance(definition, dict):
            continue
        asset_directory = str(definition.get("test_asset_directory", "")).rstrip("/")
        if asset_directory == project:
            return str(name), definition
    return None


def target_root() -> Path:
    """Resolve the external target checkout directory without saving personal state in config."""
    registry = load_json(TARGETS_PATH, {})
    if not isinstance(registry, dict):
        return ROOT.parent / "qa-automation-targets"
    env_name = str(registry.get("target_root_env", "TARGET_ROOT"))
    configured = os.getenv(env_name)
    root = Path(configured) if configured else ROOT.parent / "qa-automation-targets"
    return root if root.is_absolute() else ROOT / root


def prepare_service(plan: dict[str, object], enabled: bool) -> ServicePreflight:
    """Run the opt-outable local service preflight for the plan's registered target."""
    matched = target_for_plan(plan)
    if not enabled:
        target_name = matched[0] if matched else "none"
        return ServicePreflight(target_name, "skipped", "命令行参数要求跳过服务预检")
    if matched is None:
        return ServicePreflight("none", "skipped", "当前计划没有匹配的目标登记")
    target_name, definition = matched
    return ensure_target_service(
        target_name,
        definition,
        target_root=target_root(),
    )


def execute_day(
    day: int,
    target_command: str | None = None,
    full_command: str | None = None,
    ensure_service: bool = True,
) -> dict:
    started = time.monotonic()
    curriculum = load_json(CURRICULUM_PATH, {})
    plan = plan_for_day(curriculum, day)
    # 重新计算默认全量命令，确保 runner 与计划字段保持一致。
    plan["full_run"] = plan.get("full_run") or default_full_run(plan)
    python_path = project_python()

    target_actual, target_display = prepare_command(
        target_command or plan["run"],
        python_path,
    )
    full_actual, full_display = prepare_command(
        full_command or plan["full_run"],
        python_path,
    )

    fingerprint = project_fingerprint(ROOT, plan["test_project"])
    service = prepare_service(plan, ensure_service)
    if service.ok:
        if target_actual == full_actual:
            target_result, return_code = run_command(target_actual, target_display)
            full_result = target_result
            full_return_code = return_code
        else:
            target_result, return_code = run_command(target_actual, target_display)
            full_result, full_return_code = run_command(full_actual, full_display)
    else:
        preflight_result = f"exit_code=125 (failed)\nservice_preflight={service.evidence_line()}"
        target_result = preflight_result
        full_result = preflight_result
        return_code = 125
        full_return_code = 125

    record = {
        "version": 1,
        "run_id": uuid4().hex,
        "day": day,
        "source": "runner",
        "test_project": plan["test_project"],
        "python": str(python_path),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "duration_seconds": round(time.monotonic() - started, 2),
        "project_fingerprint": fingerprint,
        "service": service.evidence_line(),
        "target": {
            "planned_command": target_command or plan["run"],
            "command": target_display,
            "exit_code": return_code,
            "output": target_result,
        },
        "regression": {
            "planned_command": full_command or plan["full_run"],
            "command": full_display,
            "exit_code": full_return_code,
            "output": full_result,
        },
    }
    save_record(plan, record)
    return record


def save_record(plan: dict, record: dict) -> None:
    day = plan["day"]
    evidence = verification_path(day)
    evidence.parent.mkdir(parents=True, exist_ok=True)
    key_checks = existing_notes(evidence, "## 关键验证") or "\n".join(
        [
            "- 本次运行记录见下方机器记录；请教练补充与本课目标相关的关键检查。",
        ]
    )
    environment_notes = existing_notes(evidence, "## 环境问题与结论") or "\n".join(
        [
            f"- 工作目录：`{ROOT}`。",
            "- 失败需先记录根因、修复或当前阻塞，再完成当天学习。",
        ]
    )
    # Replace the machine summary on every run; retain separately written human analysis.
    environment_notes = "\n".join(
        line for line in environment_notes.splitlines() if not line.startswith("- 本次运行：")
    )
    environment_notes += (
        f"\n- 本次运行：{record['run_id']}，来源 {record['source']}，"
        f"时间 {record['finished_at']}；target={record['target']['exit_code']}，"
        f"regression={record['regression']['exit_code']}。"
    )
    evidence.write_text(
        render_verification(
            {**plan, "project": plan["test_project"]},
            target_command=record["target"]["command"],
            target_result=record["target"]["output"],
            full_command=record["regression"]["command"],
            full_result=record["regression"]["output"],
            key_checks=key_checks,
            environment_notes=environment_notes,
        ),
        encoding="utf-8",
    )

    atomic_json(evidence.parent / "runs" / record["run_id"] / "result.json", record)
    atomic_json(evidence.parent / "run-record.json", record)


def run_day(
    day: int,
    target_command: str | None = None,
    full_command: str | None = None,
    ensure_service: bool = True,
) -> int:
    record = execute_day(day, target_command, full_command, ensure_service)
    print(f"已写入：{verification_path(day)}")
    print(f"目标测试：exit_code={record['target']['exit_code']}")
    print(f"全量回归：exit_code={record['regression']['exit_code']}")
    return 0 if all(record[k]["exit_code"] == 0 for k in ("target", "regression")) else 1


def import_learner_result(day: int, path: Path) -> dict:
    """Preserve the provenance of manually supplied results."""
    plan = plan_for_day(load_json(CURRICULUM_PATH, {}), day)
    record = json.loads(path.read_text(encoding="utf-8"))
    if record.get("day") != day or record.get("test_project") != plan["test_project"]:
        raise ValueError("导入记录的学习日或项目不匹配")
    if not record.get("finished_at") or not record.get("provenance"):
        raise ValueError("导入需提供实际执行时间 finished_at 和来源说明 provenance")
    if record.get("project_fingerprint") != project_fingerprint(ROOT, plan["test_project"]):
        raise ValueError("导入代码指纹不匹配；先确认输出对应当前代码，再记录指纹")
    for kind, command in (("target", plan["run"]), ("regression", plan["full_run"])):
        run = record.get(kind, {})
        if run.get("planned_command") != command or type(run.get("exit_code")) is not int:
            raise ValueError(f"{kind} 命令或退出码无效")
        if not run.get("output") or not run.get("command"):
            raise ValueError(f"{kind} 缺少实际命令和输出")
        run["output"] = redact_output(run["output"])
    record.update(source="learner", run_id=uuid4().hex, version=1)
    save_record(plan, record)
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("day", type=int, help="学习日编号，例如 48")
    parser.add_argument(
        "--import-result", type=Path, help="导入教练根据学习者原始输出整理的 JSON 记录"
    )
    parser.add_argument(
        "--target-command",
        help="覆盖计划中的目标测试命令",
    )
    parser.add_argument(
        "--full-command",
        help="覆盖计划中的全量回归命令",
    )
    parser.add_argument(
        "--skip-service",
        action="store_true",
        help="跳过已登记本地目标的服务预检和按需启动",
    )
    args = parser.parse_args()
    if args.import_result:
        import_learner_result(args.day, args.import_result)
        print("已导入学习者结果；执行结果与课程验收分开判断。")
        return 0
    return run_day(
        args.day,
        args.target_command,
        args.full_command,
        ensure_service=not args.skip_service,
    )


if __name__ == "__main__":
    raise SystemExit(main())
