"""Generate rolling project lessons, preserving completed entries verbatim."""

import json
from pathlib import Path

from learning_workflow import load_workflow

ROOT = Path(__file__).resolve().parents[1]
LEGACY_METHOD = dict(
    study_minutes=20, practice_minutes=50, verification_minutes=15, reflection_minutes=5
)
DAILY_METHOD = dict(
    study_minutes=30,
    practice_minutes=40,
    verification_minutes=25,
    review_minutes=25,
    reflection_minutes=15,
)
PROJECT_STATUS_LABELS = {
    "completed": "已完成",
    "in_progress": "学习中",
    "pending_discovery": "待勘察",
}


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def save(path, value):
    with (ROOT / path).open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def lesson_contract(task):
    """Derive a backwards-compatible contract; new lessons should set fields explicitly."""
    run = str(task.get("run", ""))
    output = str(task.get("file", ""))
    executable = "pytest" in run or output.endswith((".py", ".js", ".ts", ".tsx"))
    lesson_type = task.get("lesson_type", "coding" if executable else "analysis")
    return {
        "lesson_type": lesson_type,
        "competency": task.get("competency", task["learn"]),
        "required_artifact_type": task.get(
            "required_artifact_type", "test" if executable else "analysis"
        ),
        "validation_mode": task.get(
            "validation_mode", "integration" if executable else "repository"
        ),
        "service_mode": task.get("service_mode", "observe"),
        "requires_executable": task.get("requires_executable", executable),
        "requires_independent_implementation": task.get(
            "requires_independent_implementation", False
        ),
        "prohibited_conclusions": task.get("prohibited_conclusions", []),
    }


def format_day_ranges(days):
    """Render sorted day numbers as compact, continuous ranges."""
    if not days:
        return "待细化"
    ranges = []
    start = previous = days[0]
    for day in days[1:]:
        if day == previous + 1:
            previous = day
            continue
        ranges.append((start, previous))
        start = previous = day
    ranges.append((start, previous))
    return "、".join(
        f"Day {start}" if start == end else f"Day {start}–{end}" for start, end in ranges
    )


def course_day_estimate(roadmap):
    """Derive the full course range from project estimates without duplicated totals."""
    estimates = [project["sessions_estimate"] for project in roadmap.get("projects", [])]
    return [sum(item[0] for item in estimates), sum(item[1] for item in estimates)]


def render_project_index(plan, roadmap):
    """Generate the single user-facing project index from the roadmap."""
    estimated_start, estimated_end = course_day_estimate(roadmap)
    lines = [
        "# 测试项目索引",
        "",
        "本索引由 `config/project-roadmap.json` 生成。项目编号表示学习顺序；",
        "只有已完成勘察并进入课程的项目才会在本目录创建测试资产。",
        "第三方被测项目源码统一放在仓库外的 `D:\\qa-automation-targets`。",
        f"当前课程已细化到 Day {len(plan)}；完整路线预计在 Day {estimated_start}–{estimated_end} 结束。",
        "",
        "| 序号 | 状态 | 项目 | 测试资产目录 | 学习日 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for project in sorted(roadmap.get("projects", []), key=lambda item: item["sequence"]):
        path = project["test_asset_directory"]
        days = sorted(
            {
                item["day"]
                for item in plan
                if path in {item.get("project"), item.get("test_project")}
            }
        )
        lines.append(
            f"| {project['sequence']:02d} | "
            f"{PROJECT_STATUS_LABELS.get(project['status'], project['status'])} | "
            f"{project['name']} | `{path}` | {format_day_ranges(days)} |"
        )
    lines.extend(
        [
            "",
            "新增项目时先完成版本、依赖、端口、契约和运行方式勘察，再更新路线图、",
            "运行目标登记和课程源配置，最后运行 `python tools/build_daily_plan.py`。",
            "待勘察项目不提前创建空目录、运行配置或学习日志。",
            "",
            "测试代码通过环境配置访问目标，不依赖第三方源码的内部绝对路径。",
            "",
        ]
    )
    return "\n".join(lines)


def build_plan():
    plan = read("docs/archive/daily-plan-v1.json")["days"][:55]
    phase = read("config/project-lessons.json")
    phases = [phase]
    phases.extend(phase.get("next_projects", []))
    day = 55
    for phase_item in phases:
        tasks = phase_item["tasks"]
        for index, task in enumerate(tasks, 1):
            day += 1
            plan.append(
                {
                    "day": day,
                    "phase_id": phase_item["id"],
                    "phase": phase_item["name"],
                    "project": phase_item["project"],
                    "objective": phase_item["objective"],
                    "phase_day": index,
                    "phase_total_days": len(tasks),
                    "week": (day - 56) // 7 + 1,
                    "timebox": dict(DAILY_METHOD),
                    "evidence": f"artifacts/day-{day:03d}/",
                    **task,
                    **lesson_contract(task),
                    "knowledge_file": task.get(
                        "knowledge_file",
                        f"docs/knowledge/day-{day:03d}.md" if day >= 77 else "LEARNING-NOTES.md",
                    ),
                    "study": f"通过需求讨论和行为预测理解：{task['learn']}。先由学习者回答，教练逐级提示。",
                    "practice": f"学习者先设计并编码：{task['deliverable']}。执行后定位问题，接受审查并亲自修改。",
                    "knowledge_check": f"不看参考答案解释“{task['learn']}”，并独立完成相似场景；记录提示程度和证据。",
                    "stretch": "改变一个业务或故障条件，独立解释结果并完成迁移",
                    "learning_output_link": f"知识：{task['learn']} → 产出：{task['deliverable']} → 验证：{task['done']}",
                }
            )
    return plan


def render_markdown(plan):
    """Render the generated Markdown plan without touching the filesystem."""
    lines = [
        "# 逐日学习计划",
        "",
        "Day 1–55 保留历史；Day 56 起每课建议 120–150 分钟，基准 135 分钟，可拆分或延长。",
        "学习与讨论 30 / 实践与实现 40 / 验证排错 25 / 审查修改 25 / 复盘 15 分钟。",
        "当前细化范围见本文，后续项目见 [路线图](ROADMAP.md)，部署勘察后追加，不自动进入旧循环。",
        "",
    ]
    phase = ""
    for item in plan:
        if item["phase"] != phase:
            phase = item["phase"]
            lines.extend([f"## {phase}", ""])
        lines.extend([f"### Day {item['day']}：{item['title']}", ""])
        for label, key in [
            ("课型", "lesson_type"),
            ("能力目标", "competency"),
            ("学习内容", "study"),
            ("场景讨论", "scenario"),
            ("动手实践", "practice"),
            ("可提交产出", "deliverable"),
            ("目标文件", "file"),
            ("知识→产出对应", "learning_output_link"),
            ("知识验收", "knowledge_check"),
            ("运行验证", "run"),
            ("验证层", "validation_mode"),
            ("完成标准", "done"),
            ("证据目录", "evidence"),
            ("知识文件", "knowledge_file"),
            ("可选挑战", "stretch"),
        ]:
            if key in item:
                lines.append(f"- {label}：{item[key]}")
        lines.append("")
    return "\n".join(lines)


def write_outputs(plan):
    workflow = load_workflow(ROOT)
    roadmap = read("config/project-roadmap.json")
    save(
        "daily-plan.json",
        dict(
            core_days=len(plan),
            planning_mode="rolling",
            session_minutes=sum(DAILY_METHOD.values()),
            session_range_minutes=[120, 150],
            daily_method=DAILY_METHOD,
            evidence_rules_from_day=workflow.get("evidence_rules_from_day"),
            days=plan,
        ),
    )
    phases = read("docs/archive/curriculum-v1.json")["phases"][:3]
    phases[2]["days"] = 20
    phase = read("config/project-lessons.json")
    phase_configs = [phase, *phase.get("next_projects", [])]
    phases.extend(
        {k: phase_item[k] for k in ("id", "name", "project", "objective")}
        | {"days": len(phase_item["tasks"])}
        for phase_item in phase_configs
    )
    save(
        "curriculum.json",
        dict(
            schema_version=2,
            planning_mode="rolling",
            core_days=len(plan),
            core_days_meaning="已细化课程范围，非整个学习路线总长度",
            preserved_through_day=55,
            roadmap="config/project-roadmap.json",
            daily_output=dict(
                time_box_minutes=sum(DAILY_METHOD.values()),
                timebox=DAILY_METHOD,
                session_range_minutes=[120, 150],
                flexible=True,
                required=[
                    "真实知识问答",
                    "测试设计与课型匹配的实践",
                    "实际运行证据",
                    "审查与修改",
                    "独立迁移记录",
                    "知识落盘",
                    "用户确认完成后提交",
                ],
                daily_loop=[s["id"] for s in workflow["stages"]],
            ),
            learning_contract=dict(
                evidence_rules_from_day=workflow.get("evidence_rules_from_day"),
                lesson_types=workflow.get("lesson_types", []),
                artifact_types=workflow.get("artifact_types", []),
                mastery_levels=workflow.get("mastery_levels", []),
            ),
            phases=phases,
            ongoing=dict(enabled=False, tracks=[]),
        ),
    )
    with (ROOT / "DAILY-PLAN.md").open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(render_markdown(plan))
    with (ROOT / "test-projects" / "README.md").open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(render_project_index(plan, roadmap))


if __name__ == "__main__":
    write_outputs(build_plan())
    print("Generated rolling curriculum; historical progress unchanged.")
