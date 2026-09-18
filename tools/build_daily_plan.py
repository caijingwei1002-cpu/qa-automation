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


if __name__ == "__main__":
    write_outputs(build_plan())
    print("Generated rolling curriculum; historical progress unchanged.")
