"""Seven-stage learning records. Reading never starts or completes a lesson."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSISTANCE = ("none", "question", "reasoning", "example", "demonstration", "coach")
ARTIFACT_TYPES = ("analysis", "code", "configuration", "test", "report")
MASTERY_LEVELS = ("not_assessed", "assisted", "independent")
EXECUTABLE_SUFFIXES = {".py", ".js", ".ts", ".tsx", ".jsx", ".ps1"}


def project_fingerprint(root: Path, project: str) -> str:
    """Bind acceptance to test source/config, excluding caches and generated reports."""
    digest = hashlib.sha256()
    base = (root / project).resolve()
    if not base.is_relative_to(root.resolve()) or not base.is_dir():
        raise ValueError(f"执行项目不存在或超出仓库：{project}")
    for path in sorted(base.rglob("*")):
        if any(
            part.startswith(".") or part == "__pycache__" for part in path.relative_to(base).parts
        ):
            continue
        if path.is_file() and (
            path.suffix
            in (
                ".py",
                ".ini",
                ".json",
                ".toml",
                ".yaml",
                ".yml",
                ".js",
                ".ts",
                ".tsx",
                ".jsx",
                ".ps1",
                ".md",
            )
            or path.name == "requirements.txt"
        ):
            digest.update(path.relative_to(base).as_posix().encode())
            digest.update(path.read_bytes())
    return digest.hexdigest()


def load_workflow(root: Path = ROOT) -> dict[str, Any]:
    return json.loads((root / "config/learning-workflow.json").read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    """Replace one JSON file atomically; never leave a partially written document."""
    path.parent.mkdir(parents=True, exist_ok=True)
    name = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=path.name,
            suffix=".tmp",
            delete=False,
        ) as stream:
            name = stream.name
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if name and Path(name).exists():
            Path(name).unlink()


def write_text_lf(path: Path, text: str) -> None:
    """Write UTF-8 text with deterministic LF endings on every platform."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(text)


def session_path(root: Path, day: int) -> Path:
    return root / "daily-log" / f"day-{day:03d}.session.json"


def read_session(root: Path, day: int) -> dict[str, Any]:
    path = session_path(root, day)
    if path.exists():
        value = json.loads(path.read_text(encoding="utf-8"))
        if value.get("day") != day or value.get("version") != load_workflow(root)["version"]:
            raise ValueError("步骤记录的学习日或版本不匹配，请先检查记录")
        return value
    return {"version": load_workflow(root)["version"], "day": day, "stages": {}, "history": []}


def session_summary(root: Path, day: int) -> dict[str, Any]:
    config = load_workflow(root)
    session = read_session(root, day)
    current = next(
        (
            s["id"]
            for s in config["stages"]
            if session["stages"].get(s["id"], {}).get("status") != "done"
        ),
        None,
    )
    return {
        **session,
        "current_stage": current,
        "workflow": config["stages"],
        "required": day >= config["required_from_day"],
    }


def record_errors(
    root: Path,
    stage: str,
    record: dict[str, Any],
    *,
    day: int | None = None,
) -> list[str]:
    errors = []
    if record.get("status") not in ("done", "in_progress"):
        errors.append("status 必须为 done 或 in_progress")
    if not str(record.get("note", "")).strip():
        errors.append("必须记录实际进展或卡点 note")
    if record.get("assistance") not in ASSISTANCE:
        errors.append("必须如实记录 assistance")
    for reference in record.get("evidence", []):
        path = (root / reference).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            errors.append(f"证据必须为仓库中已有文件：{reference}")
    if record.get("status") != "done":
        return errors
    if stage in ("preflight", "discussion", "design", "reflection"):
        if not str(record.get("learner_response", "")).strip():
            errors.append("必须记录学习者实际回答 learner_response")
    if stage in ("practice", "verification") and not record.get("evidence"):
        errors.append("必须引用实际产出或验证证据 evidence")
    if stage == "verification" and record.get("outcome") not in ("passed", "known_failure"):
        errors.append("验证尚未通过或解释清楚；blocked 应保存为 in_progress")
    if stage == "review":
        for field in ("review_result", "transfer_prompt", "transfer_response"):
            if not str(record.get(field, "")).strip():
                errors.append(f"审查和迁移缺少 {field}")
        if record.get("transfer_assistance") != "none":
            errors.append("迁移获得提示后需另设陌生场景，不能记为独立通过")
    if stage == "reflection" and not str(record.get("confirmation", "")).strip():
        errors.append("缺少学习者明确完成确认原话 confirmation")
    strict_from = int(load_workflow(root).get("evidence_rules_from_day", 10**9))
    if day is not None and day >= strict_from:
        if stage == "practice":
            if record.get("artifact_type") not in ARTIFACT_TYPES:
                errors.append("实践必须记录有效 artifact_type")
            for field in ("learner_contribution", "coach_contribution"):
                if not str(record.get(field, "")).strip():
                    errors.append(f"实践必须记录 {field}")
        if stage == "verification" and not str(record.get("verification_scope", "")).strip():
            errors.append("验证必须记录 verification_scope")
        if stage in ("review", "reflection"):
            if record.get("mastery_level") not in MASTERY_LEVELS:
                errors.append(f"{stage} 必须记录有效 mastery_level")
        if stage == "review":
            for field in ("learner_contribution", "coach_contribution"):
                if not str(record.get(field, "")).strip():
                    errors.append(f"审查必须记录 {field}")
    return errors


def checkpoint(root: Path, day: int, stage: str, record: dict[str, Any]) -> dict[str, Any]:
    progress = json.loads((root / "progress.json").read_text(encoding="utf-8"))
    if day != progress["current_day"] or day in progress["completed_days"]:
        raise ValueError("只能记录当前未完成学习日；历史更正请写明更正依据")
    order = [s["id"] for s in load_workflow(root)["stages"]]
    if stage not in order:
        raise ValueError(f"未知步骤：{stage}")
    session = read_session(root, day)
    index = order.index(stage)
    for previous in order[:index]:
        if session["stages"].get(previous, {}).get("status") != "done":
            raise ValueError(f"请先完成 {previous}，不能跳步")
    errors = record_errors(root, stage, record, day=day)
    if errors:
        raise ValueError("；".join(errors))
    if stage == "verification" and record["status"] == "done":
        result_path = root / f"artifacts/day-{day:03d}/run-record.json"
        if not result_path.is_file():
            raise ValueError("先执行统一验证或导入学习者实际结果，再记录验证完成")
        result = json.loads(result_path.read_text(encoding="utf-8"))
        record = {**record, "run_id": result.get("run_id")}
    # A changed design or implementation invalidates downstream acceptance.
    previous = {
        key: session["stages"].pop(key) for key in order[index:] if key in session["stages"]
    }
    timestamp = datetime.now(timezone.utc).isoformat()
    session["history"].append({"at": timestamp, "stage": stage, "superseded": previous})
    session["stages"][stage] = {**record, "updated_at": timestamp}
    atomic_json(session_path(root, day), session)
    return session_summary(root, day)


def completion_errors(root: Path, day: int, plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    workflow = load_workflow(root)
    if day < workflow["required_from_day"]:
        return errors
    session = read_session(root, day)
    for stage in workflow["stages"]:
        record = session["stages"].get(stage["id"], {})
        if record.get("status") != "done":
            errors.append(f"未完成步骤：{stage['title']}")
        else:
            errors.extend(record_errors(root, stage["id"], record, day=day))
    # Machine results and learner participation are independent evidence.
    path = root / f"artifacts/day-{day:03d}/run-record.json"
    if not path.is_file():
        errors.append("缺少结构化运行记录，请运行 run_day_verification.py")
        return errors
    result = json.loads(path.read_text(encoding="utf-8"))
    if result.get("day") != day or result.get("test_project") != plan["test_project"]:
        errors.append("运行记录的学习日或执行项目不匹配")
    if result.get("source") not in ("runner", "learner"):
        errors.append("运行记录必须注明来源 runner 或 learner")
    if not result.get("run_id"):
        errors.append("缺少运行编号 run_id")
    if result.get("source") == "learner" and not str(result.get("provenance", "")).strip():
        errors.append("学习者导入记录缺少来源说明 provenance")
    if result.get("project_fingerprint") != project_fingerprint(root, plan["test_project"]):
        errors.append("测试代码或配置已变化，请重新验证并更新步骤记录")
    outcome = session["stages"].get("verification", {}).get("outcome")
    if session["stages"].get("verification", {}).get("run_id") != result.get("run_id"):
        errors.append("运行记录已更新，请重新分析验证结果并验收后续步骤")
    for kind, command in (("target", plan["run"]), ("regression", plan["full_run"])):
        run = result.get(kind, {})
        if run.get("planned_command") != command:
            errors.append(f"{kind} 命令与当前计划不匹配")
        if type(run.get("exit_code")) is not int:
            errors.append(f"{kind} 缺少退出码")
        elif run["exit_code"] != 0 and outcome != "known_failure":
            errors.append(f"{kind} 未通过，需分析并明确记录 known_failure")
        elif run["exit_code"] not in (0, 1):
            errors.append(f"{kind} 执行未正常结束，不能作为已验收的业务失败")
        if not str(run.get("output", "")).strip():
            errors.append(f"{kind} 缺少实际输出")
    if not result.get("finished_at"):
        errors.append("缺少执行时间")
    strict_from = int(workflow.get("evidence_rules_from_day", 10**9))
    if day >= strict_from:
        lesson_type = plan.get("lesson_type")
        if lesson_type not in workflow.get("lesson_types", []):
            errors.append("课程缺少有效 lesson_type")
        practice = session["stages"].get("practice", {})
        review = session["stages"].get("review", {})
        verification = session["stages"].get("verification", {})
        required_artifact = plan.get("required_artifact_type")
        if practice.get("artifact_type") != required_artifact:
            errors.append("实践产物类型与课程要求不匹配")
        if verification.get("verification_scope") != plan.get("validation_mode"):
            errors.append("验证范围与课程 validation_mode 不匹配")
        if result.get("service_mode") != plan.get("service_mode"):
            errors.append("运行记录 service_mode 与课程不匹配")
        if plan.get("requires_executable"):
            if str(plan.get("run", "")).strip() == "git diff --check":
                errors.append("可执行课程不能用 git diff --check 代替目标测试")
            executable_evidence = [
                root / reference
                for reference in practice.get("evidence", [])
                if (root / reference).suffix.lower() in EXECUTABLE_SUFFIXES
            ]
            if not executable_evidence:
                errors.append("可执行课程缺少代码或测试实现证据")
            target_output = str(result.get("target", {}).get("output", ""))
            if "pytest" in str(plan.get("run", "")) and not any(
                marker in target_output.lower()
                for marker in (" passed", " failed", " error", " errors")
            ):
                errors.append("pytest 目标验证缺少测试收集或执行汇总")
        if plan.get("requires_independent_implementation"):
            if review.get("mastery_level") != "independent":
                errors.append("本课要求独立实现，但审查未达到 independent")
            if review.get("transfer_assistance") != "none":
                errors.append("独立实现迁移不能带提示")
    return errors
