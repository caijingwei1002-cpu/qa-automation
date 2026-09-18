"""Behavioral tests in disposable repositories; never advance the learner's real day."""

import argparse
import copy
import json
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import learning_workflow as workflow
import plan_day as planner
import run_day_verification as runner

REAL_RUN_COMMAND = runner.run_command


@pytest.fixture
def lab(tmp_path, monkeypatch):
    source = Path(__file__).resolve().parents[1]
    for name in (
        "config/learning-workflow.json",
        "templates/daily-log.md",
        "templates/verification.md",
    ):
        dest = tmp_path / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((source / name).read_bytes())
    project = "test-projects/demo"
    (tmp_path / project / "tests").mkdir(parents=True)
    (tmp_path / project / "tests/test_demo.py").write_text("def test_demo():\n    assert True\n")
    workflow.atomic_json(
        tmp_path / "progress.json", {"current_day": 67, "completed_days": [66], "history": []}
    )
    plan = {
        "day": 67,
        "project": project,
        "test_project": project,
        "phase": "demo",
        "theme": "示例",
        "run": f"pytest {project}/tests/test_demo.py -q",
        "full_run": f"pytest {project}/tests -q",
        "learn": "示例知识",
        "task": "示例任务",
        "deliverable": "示例产出",
        "done": "示例完成",
        "study": "学习",
        "practice": "实践",
        "file": f"{project}/tests/test_demo.py",
    }
    plan = planner.enrich_daily_plan(plan)
    for name, suffix in (
        ("ROOT", ""),
        ("PROGRESS_PATH", "progress.json"),
        ("LOG_DIR", "daily-log"),
        ("ARTIFACT_DIR", "artifacts"),
        ("TEMPLATE_PATH", "templates/daily-log.md"),
        ("VERIFICATION_TEMPLATE_PATH", "templates/verification.md"),
    ):
        monkeypatch.setattr(planner, name, tmp_path / suffix)
    monkeypatch.setattr(planner, "plan_for_day", lambda _curriculum, _day: dict(plan))
    monkeypatch.setattr(runner, "ROOT", tmp_path)
    monkeypatch.setattr(runner, "plan_for_day", lambda _curriculum, _day: dict(plan))
    monkeypatch.setattr(
        runner,
        "prepare_service",
        lambda *_: runner.ServicePreflight("demo", "skipped", "unit fixture"),
    )
    monkeypatch.setattr(runner, "run_command", Mock(return_value=("1 passed", 0)))
    return tmp_path, plan


def step_record(stage):
    return {
        "status": "done",
        "note": "实际进展",
        "assistance": "none",
        "learner_response": "实际回答",
        "evidence": ["test-projects/demo/tests/test_demo.py"],
        "outcome": "passed",
        "review_result": "自审发现遗漏，补充后复审通过",
        "transfer_prompt": "换一种输入如何处理？",
        "transfer_response": "独立方案",
        "transfer_assistance": "none",
        "confirmation": "完成当天",
    }


def finish_stages(root):
    for stage in workflow.load_workflow(root)["stages"]:
        workflow.checkpoint(root, 67, stage["id"], step_record(stage["id"]))


def write_knowledge(root, plan):
    notes = "# 知识库\n\n- [Day 67：示例](#day-67示例)\n\n## Day 67：示例\n"
    for heading in ("核心知识点", "它解决的问题", "理论基础", "代码落地", "知识验收", "关联产出"):
        notes += f"\n### {heading}\n\n实际内容\n"
    notes += "\n## 知识主题索引\n\nDay 67\n"
    (root / "LEARNING-NOTES.md").write_text(notes, encoding="utf-8")
    planner.write_daily_log(plan)


def test_read_only_session_does_not_start_day(lab):
    root, _ = lab
    assert workflow.session_summary(root, 67)["current_stage"] == "preflight"
    assert not (root / "daily-log").exists()


def test_no_jumping_and_resume_saved_work(lab):
    root, _ = lab
    with pytest.raises(ValueError, match="preflight"):
        workflow.checkpoint(root, 67, "design", step_record("design"))
    record = {**step_record("preflight"), "status": "in_progress", "next_action": "继续复习"}
    workflow.checkpoint(root, 67, "preflight", record)
    summary = workflow.session_summary(root, 67)
    assert summary["current_stage"] == "preflight"
    assert summary["stages"]["preflight"]["next_action"] == "继续复习"


def test_changing_earlier_step_invalidates_later_acceptance(lab):
    root, _ = lab
    runner.execute_day(67)
    finish_stages(root)
    workflow.checkpoint(root, 67, "design", {**step_record("design"), "note": "修改断言设计"})
    summary = workflow.session_summary(root, 67)
    assert summary["current_stage"] == "practice"
    assert "reflection" not in summary["stages"]
    assert "reflection" in summary["history"][-1]["superseded"]


def test_assisted_transfer_and_missing_confirmation_rejected(lab):
    root, _ = lab
    assert workflow.record_errors(
        root, "review", {**step_record("review"), "transfer_assistance": "example"}
    )
    assert workflow.record_errors(
        root, "reflection", {**step_record("reflection"), "confirmation": ""}
    )


def test_missing_or_outside_evidence_rejected(lab):
    root, _ = lab
    for reference in ("missing.py", "../outside.py"):
        assert workflow.record_errors(
            root, "practice", {**step_record("practice"), "evidence": [reference]}
        )


def test_complete_checks_before_writing_and_is_idempotent(lab):
    root, plan = lab
    args = argparse.Namespace(day=67, result="完成", next_step="下一课")
    before = (root / "progress.json").read_bytes()
    with pytest.raises(ValueError, match="校验失败"):
        planner.command_complete(args)
    assert (root / "progress.json").read_bytes() == before
    assert not (root / "daily-log").exists()
    runner.execute_day(67)
    finish_stages(root)
    write_knowledge(root, plan)
    planner.command_complete(args)
    completed = (root / "progress.json").read_bytes()
    assert json.loads(completed)["current_day"] == 68
    planner.command_complete(args)
    assert (root / "progress.json").read_bytes() == completed
    assert len(json.loads(completed)["history"]) == 1


def test_future_completion_cannot_skip_current_day(lab):
    root, _ = lab
    before = (root / "progress.json").read_bytes()
    with pytest.raises(ValueError, match="不能跳过"):
        planner.command_complete(argparse.Namespace(day=68, result="完成", next_step=""))
    assert (root / "progress.json").read_bytes() == before


def test_structured_results_reject_wrong_commands_and_stale_code(lab):
    root, plan = lab
    record = runner.execute_day(67)
    finish_stages(root)
    assert workflow.completion_errors(root, 67, plan) == []
    record["regression"]["planned_command"] = "pytest another-project"
    workflow.atomic_json(root / "artifacts/day-067/run-record.json", record)
    assert any("命令" in e for e in workflow.completion_errors(root, 67, plan))
    runner.execute_day(67)
    finish_stages(root)
    (root / plan["file"]).write_text("def test_demo():\n    assert False\n")
    assert any("代码或配置" in e for e in workflow.completion_errors(root, 67, plan))


def test_rerun_requires_reacceptance_and_failure_requires_explanation(lab, monkeypatch):
    root, plan = lab
    runner.execute_day(67)
    finish_stages(root)
    monkeypatch.setattr(runner, "run_command", Mock(return_value=("1 failed", 1)))
    runner.execute_day(67)
    assert any("记录已更新" in e for e in workflow.completion_errors(root, 67, plan))
    assert any("未通过" in e for e in workflow.completion_errors(root, 67, plan))
    workflow.checkpoint(
        root,
        67,
        "verification",
        {
            **step_record("verification"),
            "outcome": "known_failure",
            "note": "已复现业务缺陷并记录契约依据",
        },
    )
    for step in ("review", "reflection"):
        workflow.checkpoint(root, 67, step, step_record(step))
    assert workflow.completion_errors(root, 67, plan) == []


def test_runner_saves_distinct_runs_and_matching_summary(lab):
    root, plan = lab
    first = runner.execute_day(67)
    second = runner.execute_day(67)
    runs = list((root / "artifacts/day-067/runs").glob("*/result.json"))
    assert len(runs) == 2
    assert first["run_id"] != second["run_id"]
    summary = (root / "artifacts/day-067/verification.md").read_text(encoding="utf-8")
    assert second["run_id"] in summary and first["run_id"] not in summary
    assert plan["test_project"] in summary


def test_import_cannot_claim_runner_provenance(lab):
    root, _ = lab
    record = runner.execute_day(67)
    record["provenance"] = "学习者 PowerShell 输出，对应当前代码"
    path = root / "import.json"
    workflow.atomic_json(path, record)
    imported = runner.import_learner_result(67, path)
    assert imported["source"] == "learner"
    assert imported["run_id"] != record["run_id"]


def test_cross_project_lesson_routes_ui_regression_and_service():
    source = Path(__file__).resolve().parents[1]
    days = json.loads((source / "daily-plan.json").read_text(encoding="utf-8"))["days"]
    plan = planner.enrich_daily_plan(copy.deepcopy(days[65]))
    assert plan["full_run"] == "pytest test-projects/02-saucedemo-ui/tests -q"
    assert runner.target_for_plan(plan)[0] == "saucedemo"


def test_timeout_preserves_partial_bytes_output(lab, monkeypatch):
    import subprocess

    monkeypatch.setattr(runner, "run_command", REAL_RUN_COMMAND)
    monkeypatch.setattr(
        runner.subprocess,
        "run",
        Mock(
            side_effect=subprocess.TimeoutExpired("pytest", 1, output=b"partial", stderr=b"error")
        ),
    )
    output, code = runner.run_command(["pytest"], "pytest", timeout=1)
    assert code == 124
    assert "partial" in output and "error" in output


def test_runner_captures_real_local_pytest_result(lab, monkeypatch):
    root, _ = lab
    monkeypatch.setattr(runner, "run_command", REAL_RUN_COMMAND)
    result = runner.execute_day(67)
    assert result["target"]["exit_code"] == 0
    assert result["regression"]["exit_code"] == 0
    assert "1 passed" in result["target"]["output"]
    assert (root / "artifacts/day-067/run-record.json").is_file()


def test_mcp_routes_read_and_verification_to_shared_commands(monkeypatch):
    import importlib.util

    source = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "qa_learning_mcp_test", source / "plugins/qa-learning-coach/scripts/qa_learning_mcp.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    dispatch = Mock(return_value={"output": "ok"})
    monkeypatch.setattr(module, "run_planner", dispatch)
    args = {"day": 67}
    module.tool_result("get_today_plan", args)
    dispatch.assert_called_with(args, "show")
    module.tool_result("verify_learning_day", args)
    dispatch.assert_called_with(args, "verify", "67")
    args["record"] = {
        "note": "学习者的实际回答",
        "assistance": "none",
        "learner_response": "边界输入",
    }
    args["stage"] = "design"
    module.tool_result("record_learning_step", args)
    dispatch.assert_called_with(
        args,
        "checkpoint",
        "67",
        "design",
        "--note",
        "学习者的实际回答",
        "--assistance",
        "none",
        "--learner-response",
        "边界输入",
    )
