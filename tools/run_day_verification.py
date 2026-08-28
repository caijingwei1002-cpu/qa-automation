#!/usr/bin/env python3
"""Run the daily checks and write the standard verification.md evidence."""

from __future__ import annotations

import argparse
import re
import shlex
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from plan_day import (  # noqa: E402
    CURRICULUM_PATH,
    default_full_run,
    load_json,
    plan_for_day,
    render_verification,
    verification_path,
)


SENSITIVE_VALUE = re.compile(
    r'''(?i)(["']?(?:token|password|authorization|cookie)["']?\s*[:=]\s*["']?)([^"'\s,;}]+)'''
)


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
    next_heading = re.search(r"\n## ", text[start + len(heading):])
    end = start + len(heading) + next_heading.start() if next_heading else len(text)
    body = text[start + len(heading):end].strip()
    if not body or any(marker in body for marker in ("待补充", "待记录", "待填写")):
        return None
    return body


def run_command(actual: list[str], display: str) -> tuple[str, int]:
    """执行命令并生成可写入证据的结果文本。"""
    try:
        completed = subprocess.run(
            actual,
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        output = "\n".join(
            part for part in (completed.stdout.strip(), completed.stderr.strip()) if part
        )
        output = redact_output(output) or "<no output>"
        status = "passed" if completed.returncode == 0 else "failed"
        return f"exit_code={completed.returncode} ({status})\n{output}", completed.returncode
    except OSError as exc:
        return (
            f"exit_code=127 (failed)\ncommand={display}\n"
            f"error={exc.__class__.__name__}: {exc}",
            127,
        )


def run_day(
    day: int,
    target_command: str | None = None,
    full_command: str | None = None,
) -> int:
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

    if target_actual == full_actual:
        target_result, return_code = run_command(target_actual, target_display)
        full_result = target_result
        full_return_code = return_code
    else:
        target_result, return_code = run_command(target_actual, target_display)
        full_result, full_return_code = run_command(full_actual, full_display)

    evidence = verification_path(day)
    evidence.parent.mkdir(parents=True, exist_ok=True)
    key_checks = existing_notes(evidence, "## 关键验证") or "\n".join(
        [
            f"- 目标测试退出码：`{return_code}`。",
            f"- 全量回归退出码：`{full_return_code}`。",
            "- 测试命令由本运行脚本绑定到仓库虚拟环境。",
        ]
    )
    environment_notes = existing_notes(evidence, "## 环境问题与结论") or "\n".join(
        [
            f"- 工作目录：`{ROOT}`。",
            f"- 测试解释器：`{python_path}`。",
            "- 结论：结果已由命令真实执行并写入本文件；如有失败，应先记录根因再完成当天学习。",
        ]
    )
    evidence.write_text(
        render_verification(
            plan,
            target_command=target_display,
            target_result=target_result,
            full_command=full_display,
            full_result=full_result,
            key_checks=key_checks,
            environment_notes=environment_notes,
        ),
        encoding="utf-8",
    )

    print(f"已写入：{evidence}")
    print(f"目标测试：exit_code={return_code}")
    print(f"全量回归：exit_code={full_return_code}")
    return 0 if return_code == 0 and full_return_code == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("day", type=int, help="学习日编号，例如 48")
    parser.add_argument(
        "--target-command",
        help="覆盖计划中的目标测试命令",
    )
    parser.add_argument(
        "--full-command",
        help="覆盖计划中的全量回归命令",
    )
    args = parser.parse_args()
    return run_day(args.day, args.target_command, args.full_command)


if __name__ == "__main__":
    raise SystemExit(main())
