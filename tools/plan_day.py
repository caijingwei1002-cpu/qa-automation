#!/usr/bin/env python3
"""Plan, record, and review daily QA automation learning work."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_daily_plan import DAILY_METHOD  # noqa: E402


CURRICULUM_PATH = ROOT / "curriculum.json"
DAILY_PLAN_PATH = ROOT / "daily-plan.json"
PROGRESS_PATH = ROOT / "progress.json"
LOG_DIR = ROOT / "daily-log"
ARTIFACT_DIR = ROOT / "artifacts"
TEMPLATE_PATH = ROOT / "templates" / "daily-log.md"
def load_json(path: Path, default: Any) -> Any:
    """读取 UTF-8 JSON；文件不存在时返回调用方提供的默认结构。"""
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_progress() -> dict[str, Any]:
    """读取进度并补齐旧版本文件可能缺少的默认字段。"""
    progress = load_json(
        PROGRESS_PATH,
        {"current_day": 1, "completed_days": [], "history": []},
    )
    progress.setdefault("current_day", 1)
    progress.setdefault("completed_days", [])
    progress.setdefault("history", [])
    return progress


def enrich_daily_plan(plan: dict[str, Any]) -> dict[str, Any]:
    """Give generated, fallback, and ongoing days the same daily contract."""
    plan.setdefault("learn", plan.get("theme", "完成一个明确的测试学习目标"))
    plan.setdefault("deliverable", plan.get("task", "完成一个可运行产出并记录证据"))
    plan.setdefault(
        "study",
        f"用 20 分钟学习一个知识重点：{plan['learn']}。写下它解决的问题和一个常见误区。",
    )
    plan.setdefault(
        "practice",
        f"用 50 分钟把知识应用到小练习：{plan['deliverable']}。只完成当天范围。",
    )
    plan.setdefault(
        "knowledge_check",
        f"不看资料，说明“{plan['learn']}”如何体现在今天的代码或文档产出中。",
    )
    plan.setdefault("timebox", dict(DAILY_METHOD))
    plan.setdefault("evidence", f"artifacts/day-{plan['day']:03d}/")
    plan.setdefault(
        "learning_output_link",
        f"知识：{plan['learn']} → 产出：{plan['deliverable']} → 验证：{plan.get('done', '运行结果与完成标准一致')}",
    )
    plan.setdefault("file", f"daily-log/day-{plan['day']:03d}.md")
    plan.setdefault("run", "git diff --check")
    plan.setdefault("done", "产出完成、命令执行并记录结果")
    plan.setdefault("stretch", "补充一个边界场景或改进建议")
    return plan


def save_progress(progress: dict[str, Any]) -> None:
    PROGRESS_PATH.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def phase_for_day(curriculum: dict[str, Any], day: int) -> tuple[dict[str, Any], int]:
    """把绝对学习日映射为所属阶段及阶段内的相对天数。"""
    remaining = day
    for phase in curriculum["phases"]:
        if remaining <= phase["days"]:
            return phase, remaining
        remaining -= phase["days"]
    raise ValueError("core curriculum is exhausted")


def plan_for_day(curriculum: dict[str, Any], day: int) -> dict[str, Any]:
    """按优先级选择详细日计划、核心回退计划或长期专项计划。"""
    core_days = curriculum["core_days"]
    if day <= 0:
        raise ValueError("day must be positive")
    detailed = load_json(DAILY_PLAN_PATH, {})
    detailed_days = detailed.get("days", [])
    if day <= len(detailed_days):
        item = dict(detailed_days[day - 1])
        # Keep the original planner shape while exposing the richer daily fields.
        item.setdefault("theme", item.get("title", "综合练习"))
        item.setdefault("task", item.get("deliverable", "完成一个可运行测试脚本并记录证据"))
        return enrich_daily_plan(item)
    if day <= core_days:
        phase, relative_day = phase_for_day(curriculum, day)
        themes = phase.get("week_themes", ["综合练习"])
        tasks = phase.get("daily_tasks", ["完成一个可运行测试脚本并记录证据"])
        theme = themes[min((relative_day - 1) // 7, len(themes) - 1)]
        task = tasks[(relative_day - 1) % len(tasks)]
        return enrich_daily_plan({
            "day": day,
            "phase": phase["name"],
            "project": phase["project"],
            "objective": phase["objective"],
            "theme": theme,
            "task": task,
            "track": "core",
        })

    ongoing = curriculum["ongoing"]
    offset = day - core_days - 1
    cycle_days = ongoing["cycle_days"]
    cycle = offset // cycle_days + 1
    within_cycle = offset % cycle_days
    tracks = ongoing["tracks"]
    track = tracks[(cycle - 1) % len(tracks)]
    task_item = track["tasks"][within_cycle % len(track["tasks"])]
    if isinstance(task_item, dict):
        task = task_item["task"]
        learn = task_item["learn"]
        deliverable = task_item["deliverable"]
        output_file = task_item["file"]
        run = task_item["run"]
    else:
        task = task_item
        learn = f"理解{track['name']}中的{task}方法与风险"
        deliverable = task
        output_file = f"daily-log/day-{day:03d}.md"
        run = "git diff --check"
    return enrich_daily_plan({
        "day": day,
        "phase": f"长期专项：{track['name']}",
        "project": "qa-automation-learning",
        "objective": "在已有项目上增加一个真实的工程改进",
        "theme": f"第 {cycle} 轮专项，第 {within_cycle + 1} 天",
        "task": task,
        "learn": learn,
        "deliverable": deliverable,
        "file": output_file,
        "run": run,
        "track": "ongoing",
    })


def render_log(plan: dict[str, Any], result: str = "", next_step: str = "") -> str:
    """将日计划字段填入日志模板，并保留固定的学习闭环结构。"""
    text = TEMPLATE_PATH.read_text(encoding="utf-8")
    replacements = {
        "{{day}}": str(plan["day"]),
        "{{date}}": date.today().isoformat(),
        "{{phase}}": plan["phase"],
        "{{project}}": plan["project"],
        "{{theme}}": plan["theme"],
        "{{learn}}": plan["learn"],
        "{{task}}": plan["task"],
        "{{evidence}}": plan["evidence"],
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    timebox = plan["timebox"]
    detail = [
        f"时间盒：学习 {timebox['study_minutes']} 分钟 + 实践 {timebox['practice_minutes']} 分钟 + 验证 {timebox['verification_minutes']} 分钟 + 复盘 {timebox['reflection_minutes']} 分钟",
        f"学习内容：{plan['study']}",
        f"动手实践：{plan['practice']}",
        f"可提交产出：{plan['deliverable']}",
        f"目标文件：`{plan['file']}`",
        f"知识→产出对应：{plan['learning_output_link']}",
        f"知识验收：{plan['knowledge_check']}",
        f"运行验证：`{plan['run']}`",
        f"完成标准：{plan['done']}",
        f"证据目录：`{plan['evidence']}`",
        f"可选挑战：{plan['stretch']}",
    ]
    text = text.replace("{{daily_detail}}", "\n".join(f"- {item}" for item in detail))
    if result:
        text = text.replace("结果：\n", f"结果：{result}\n")
    if next_step:
        text = text.replace("明天的第一步：\n", f"明天的第一步：{next_step}\n")
    return text


def fill_log_field(text: str, label: str, value: str) -> str:
    """Fill a blank log field without replacing existing notes."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line == label:
            lines[index] = f"{label}{value}"
            return "\n".join(lines) + "\n"
        if line.startswith(label):
            return text
    return text.rstrip() + f"\n\n{label}{value}\n"


def write_daily_log(plan: dict[str, Any], result: str = "", next_step: str = "") -> Path:
    """创建或增量更新日志，避免覆盖学习者已经填写的复盘内容。"""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    artifact_path = ARTIFACT_DIR / f"day-{plan['day']:03d}"
    artifact_path.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"day-{plan['day']:03d}.md"
    existing = log_path.read_text(encoding="utf-8") if log_path.exists() else ""
    old_blank_markers = (
        "今天理解了：",
        "遇到的问题：",
        "根因或当前假设：",
        "今天的最小成果：",
        "明天的第一步：",
        "提交：",
    )
    needs_template_refresh = (
        "{{daily_detail}}" in existing
        or (
            "## 今日详细计划" in existing
            and "## 今日学习与产出" not in existing
            and all(f"{marker}\n\n" in existing for marker in old_blank_markers)
        )
    )
    if result or next_step:
        updated = existing or render_log(plan)
        if result:
            updated = fill_log_field(updated, "结果：", result)
        if next_step:
            updated = fill_log_field(updated, "明天的第一步：", next_step)
        log_path.write_text(updated, encoding="utf-8")
    elif not log_path.exists() or needs_template_refresh:
        log_path.write_text(render_log(plan, result, next_step), encoding="utf-8")
    return log_path


def print_plan(plan: dict[str, Any], log_path: Path | None = None) -> None:
    print(f"Day {plan['day']} | {plan['phase']} | {plan['project']}")
    print(f"主题：{plan['theme']}")
    print(f"目标：{plan['objective']}")
    print(f"今日任务：{plan['task']}")
    print(f"学习内容：{plan['study']}")
    print(f"动手实践：{plan['practice']}")
    print(f"今日产出：{plan['deliverable']}")
    print(f"目标文件：{plan['file']}")
    print(f"知识验收：{plan['knowledge_check']}")
    print(f"运行验证：{plan['run']}")
    print(f"完成标准：{plan['done']}")
    print(f"证据目录：{plan['evidence']}")
    if log_path:
        print(f"已生成：{log_path}")


def command_today(args: argparse.Namespace) -> None:
    curriculum = load_json(CURRICULUM_PATH, {})
    progress = load_progress()
    day = progress["current_day"]
    plan = plan_for_day(curriculum, day)
    print_plan(plan, write_daily_log(plan))


def command_plan(args: argparse.Namespace) -> None:
    curriculum = load_json(CURRICULUM_PATH, {})
    plan = plan_for_day(curriculum, args.day)
    print_plan(plan, write_daily_log(plan))


def command_complete(args: argparse.Namespace) -> None:
    curriculum = load_json(CURRICULUM_PATH, {})
    progress = load_progress()
    plan = plan_for_day(curriculum, args.day)
    write_daily_log(plan, args.result, args.next_step)
    # 完成命令只追加未完成日，并将下一天推进到当前完成日之后。
    if args.day not in progress["completed_days"]:
        progress["completed_days"].append(args.day)
        progress["completed_days"].sort()
    progress["history"].append(
        {
            "day": args.day,
            "date": date.today().isoformat(),
            "result": args.result,
            "next_step": args.next_step,
        }
    )
    if args.day >= progress["current_day"]:
        progress["current_day"] = args.day + 1
    save_progress(progress)
    print(f"已完成 Day {args.day}，下一天是 Day {progress['current_day']}。")


def command_status(args: argparse.Namespace) -> None:
    curriculum = load_json(CURRICULUM_PATH, {})
    progress = load_progress()
    completed = len(progress["completed_days"])
    core = curriculum["core_days"]
    core_done = min(completed, core)
    print(f"当前学习日：Day {progress['current_day']}")
    print(f"已完成：{completed} 天（核心路线 {core_done}/{core}）")
    if completed:
        print(f"最近完成：Day {progress['completed_days'][-1]}")
    next_plan = plan_for_day(curriculum, progress["current_day"])
    print(f"下一主题：{next_plan['phase']} / {next_plan['task']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("today", help="显示并生成当前学习日")
    plan = sub.add_parser("plan", help="显示并生成指定学习日")
    plan.add_argument("day", type=int)
    complete = sub.add_parser("complete", help="完成一个学习日并记录结果")
    complete.add_argument("day", type=int)
    complete.add_argument("--result", required=True)
    complete.add_argument("--next-step", default="")
    sub.add_parser("status", help="显示累计进度")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    commands = {
        "today": command_today,
        "plan": command_plan,
        "complete": command_complete,
        "status": command_status,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
