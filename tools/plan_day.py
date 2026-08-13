#!/usr/bin/env python3
"""Plan, record, and review daily QA automation learning work."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_PATH = ROOT / "curriculum.json"
DAILY_PLAN_PATH = ROOT / "daily-plan.json"
PROGRESS_PATH = ROOT / "progress.json"
LOG_DIR = ROOT / "daily-log"
ARTIFACT_DIR = ROOT / "artifacts"
TEMPLATE_PATH = ROOT / "templates" / "daily-log.md"


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_progress() -> dict[str, Any]:
    progress = load_json(
        PROGRESS_PATH,
        {"current_day": 1, "completed_days": [], "history": []},
    )
    progress.setdefault("current_day", 1)
    progress.setdefault("completed_days", [])
    progress.setdefault("history", [])
    return progress


def save_progress(progress: dict[str, Any]) -> None:
    PROGRESS_PATH.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def phase_for_day(curriculum: dict[str, Any], day: int) -> tuple[dict[str, Any], int]:
    remaining = day
    for phase in curriculum["phases"]:
        if remaining <= phase["days"]:
            return phase, remaining
        remaining -= phase["days"]
    raise ValueError("core curriculum is exhausted")


def plan_for_day(curriculum: dict[str, Any], day: int) -> dict[str, Any]:
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
        return item
    if day <= core_days:
        phase, relative_day = phase_for_day(curriculum, day)
        themes = phase.get("week_themes", ["综合练习"])
        tasks = phase.get("daily_tasks", ["完成一个可运行测试脚本并记录证据"])
        theme = themes[min((relative_day - 1) // 7, len(themes) - 1)]
        task = tasks[(relative_day - 1) % len(tasks)]
        return {
            "day": day,
            "phase": phase["name"],
            "project": phase["project"],
            "objective": phase["objective"],
            "theme": theme,
            "task": task,
            "track": "core",
        }

    ongoing = curriculum["ongoing"]
    offset = day - core_days - 1
    cycle_days = ongoing["cycle_days"]
    cycle = offset // cycle_days + 1
    within_cycle = offset % cycle_days
    tracks = ongoing["tracks"]
    track = tracks[(cycle - 1) % len(tracks)]
    task = track["tasks"][within_cycle % len(track["tasks"])]
    return {
        "day": day,
        "phase": f"长期专项：{track['name']}",
        "project": "qa-automation-learning",
        "objective": "在已有项目上增加一个真实的工程改进",
        "theme": f"第 {cycle} 轮专项，第 {within_cycle + 1} 天",
        "task": task,
        "track": "ongoing",
    }


def render_log(plan: dict[str, Any], result: str = "", next_step: str = "") -> str:
    text = TEMPLATE_PATH.read_text(encoding="utf-8")
    replacements = {
        "{{day}}": str(plan["day"]),
        "{{date}}": date.today().isoformat(),
        "{{phase}}": plan["phase"],
        "{{project}}": plan["project"],
        "{{theme}}": plan["theme"],
        "{{task}}": plan["task"],
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    detail = []
    if plan.get("learn"):
        detail.append(f"学习重点：{plan['learn']}")
    if plan.get("deliverable"):
        detail.append(f"今日产出：{plan['deliverable']}")
    if plan.get("file"):
        detail.append(f"目标文件：`{plan['file']}`")
    if plan.get("run"):
        detail.append(f"运行命令：`{plan['run']}`")
    if plan.get("done"):
        detail.append(f"完成标准：{plan['done']}")
    if plan.get("stretch"):
        detail.append(f"可选挑战：{plan['stretch']}")
    if detail:
        text = text.replace("{{daily_detail}}", "\n".join(f"- {item}" for item in detail))
    if result:
        text = text.replace("结果：\n", f"结果：{result}\n")
    if next_step:
        text = text.replace("明天的第一步：\n", f"明天的第一步：{next_step}\n")
    return text


def write_daily_log(plan: dict[str, Any], result: str = "", next_step: str = "") -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    artifact_path = ARTIFACT_DIR / f"day-{plan['day']:03d}"
    artifact_path.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"day-{plan['day']:03d}.md"
    if not log_path.exists() or result or next_step:
        log_path.write_text(render_log(plan, result, next_step), encoding="utf-8")
    return log_path


def print_plan(plan: dict[str, Any], log_path: Path | None = None) -> None:
    print(f"Day {plan['day']} | {plan['phase']} | {plan['project']}")
    print(f"主题：{plan['theme']}")
    print(f"目标：{plan['objective']}")
    print(f"今日任务：{plan['task']}")
    if plan.get("learn"):
        print(f"学习重点：{plan['learn']}")
    if plan.get("deliverable"):
        print(f"今日产出：{plan['deliverable']}")
    if plan.get("file"):
        print(f"目标文件：{plan['file']}")
    if plan.get("run"):
        print(f"运行命令：{plan['run']}")
    if plan.get("done"):
        print(f"完成标准：{plan['done']}")
    if plan.get("stretch"):
        print(f"可选挑战：{plan['stretch']}")
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
