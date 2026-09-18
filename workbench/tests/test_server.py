from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from http import HTTPStatus
from pathlib import Path
from unittest.mock import Mock, patch

WORKBENCH_ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = WORKBENCH_ROOT / "server.py"
if str(WORKBENCH_ROOT) not in sys.path:
    sys.path.insert(0, str(WORKBENCH_ROOT))
SPEC = importlib.util.spec_from_file_location("qa_workbench_server", SERVER_PATH)
assert SPEC and SPEC.loader
server = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(server)


class PathSecurityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "test-projects" / "demo").mkdir(parents=True)
        (self.root / "daily-log").mkdir()
        (self.root / "artifacts").mkdir()
        (self.root / "progress.json").write_text("{}", encoding="utf-8")
        self.code = self.root / "test-projects" / "demo" / "test_demo.py"
        self.code.write_text("def test_demo():\n    assert True\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_allows_learning_code(self) -> None:
        resolved = server.resolve_project_path(
            self.root, "test-projects/demo/test_demo.py", write=True
        )
        self.assertEqual(resolved, self.code.resolve())

    def test_rejects_parent_traversal(self) -> None:
        with self.assertRaises(server.WorkbenchError):
            server.resolve_project_path(self.root, "../secret.txt")

    def test_rejects_sensitive_root_file(self) -> None:
        with self.assertRaises(server.WorkbenchError) as raised:
            server.resolve_project_path(self.root, ".env")
        self.assertEqual(raised.exception.status, HTTPStatus.FORBIDDEN)

    def test_root_plan_files_are_read_only(self) -> None:
        with self.assertRaises(server.WorkbenchError) as raised:
            server.resolve_project_path(self.root, "progress.json", write=True)
        self.assertEqual(raised.exception.status, HTTPStatus.FORBIDDEN)


class SaveConflictTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "test-projects").mkdir()
        self.path = self.root / "test-projects" / "sample.py"
        self.path.write_text("value = 1\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_atomic_save_with_matching_version(self) -> None:
        version = self.path.stat().st_mtime_ns
        result = server.save_text_file(self.root, "test-projects/sample.py", "value = 2\n", version)
        self.assertEqual(self.path.read_text(encoding="utf-8"), "value = 2\n")
        self.assertEqual(result["size"], len(self.path.read_bytes()))

    def test_preserves_lf_line_endings(self) -> None:
        self.path.write_bytes(b"value = 1\n")
        version = self.path.stat().st_mtime_ns
        server.save_text_file(self.root, "test-projects/sample.py", "value = 2\n", version)
        self.assertEqual(self.path.read_bytes(), b"value = 2\n")

    def test_rejects_stale_editor_content(self) -> None:
        stale_version = self.path.stat().st_mtime_ns
        self.path.write_text("changed_in_pycharm = True\n", encoding="utf-8")
        os.utime(self.path, ns=(stale_version + 10_000_000, stale_version + 10_000_000))
        with self.assertRaises(server.WorkbenchError) as raised:
            server.save_text_file(
                self.root, "test-projects/sample.py", "overwrite = True\n", stale_version
            )
        self.assertEqual(raised.exception.status, HTTPStatus.CONFLICT)
        self.assertIn("其他程序修改", str(raised.exception))


class SharedVerificationTests(unittest.TestCase):
    def test_regression_failure_is_returned_from_shared_runner(self) -> None:
        planner = Mock()
        planner.load_progress.return_value = {"current_day": 67}
        planner.plan_for_day.return_value = {
            "run": "pytest test-projects/demo/tests/test_demo.py -q",
            "full_run": "pytest test-projects/demo/tests -q",
        }
        planner.execute_verification.return_value = {
            "target": {"exit_code": 0, "output": "1 passed"},
            "regression": {"exit_code": 1, "output": "1 failed"},
            "duration_seconds": 2.5,
        }
        with patch.object(server, "load_planner", return_value=planner):
            result = server.run_current_tests(Path(tempfile.gettempdir()))
        planner.execute_verification.assert_called_once_with(67)
        self.assertFalse(result["passed"])
        self.assertEqual(result["returncode"], 1)
        self.assertIn("1 failed", result["output"])
        self.assertEqual(result["evidence"], "artifacts/day-067/verification.md")


class CommandAllowlistTests(unittest.TestCase):
    def test_accepts_pytest_plan(self) -> None:
        self.assertEqual(
            server.parse_allowed_pytest("pytest test-projects/demo/tests/test_demo.py -q"),
            ["test-projects/demo/tests/test_demo.py", "-q"],
        )

    def test_rejects_non_pytest_commands(self) -> None:
        with self.assertRaises(server.WorkbenchError):
            server.parse_allowed_pytest("python tools/plan_day.py complete")

    def test_rejects_shell_operators(self) -> None:
        for command in ("pytest -q; whoami", "pytest -q | more", "pytest -q && echo done"):
            with self.subTest(command=command), self.assertRaises(server.WorkbenchError):
                server.parse_allowed_pytest(command)


if __name__ == "__main__":
    unittest.main()
