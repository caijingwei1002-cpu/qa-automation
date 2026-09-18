from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


BRIDGE_PATH = Path(__file__).resolve().parents[1] / "codex_bridge.py"
SPEC = importlib.util.spec_from_file_location("qa_codex_bridge", BRIDGE_PATH)
assert SPEC and SPEC.loader
bridge_module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = bridge_module
SPEC.loader.exec_module(bridge_module)
FAKE_SERVER = Path(__file__).resolve().parent / "fake_app_server.py"


def fake_process_factory(_args, **kwargs):
    return subprocess.Popen([sys.executable, str(FAKE_SERVER)], **kwargs)


class CodexBridgeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "artifacts").mkdir()
        self.bridge = bridge_module.CodexBridge(
            self.root,
            executable=Path(sys.executable),
            process_factory=fake_process_factory,
            request_timeout=3,
        )

    def tearDown(self) -> None:
        self.bridge.stop()
        self.temporary.cleanup()

    def test_initializes_and_reads_chatgpt_account(self) -> None:
        status = self.bridge.start()
        self.assertTrue(status["running"])
        self.assertTrue(status["initialized"])
        self.assertEqual(status["account"]["type"], "chatgpt")

    def test_creates_and_persists_one_thread_per_day(self) -> None:
        self.bridge.start()
        session = self.bridge.session_for_day(30, {"title": "页面对象", "learn": "封装", "run": "pytest -q"}, bootstrap=False)
        self.assertTrue(session["created"])
        self.assertEqual(session["thread_id"], "fake-thread")
        state = json.loads((self.root / "artifacts" / "workbench-state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["days"]["30"]["thread_id"], "fake-thread")
        resumed = self.bridge.session_for_day(30, {"title": "页面对象"}, bootstrap=False)
        self.assertFalse(resumed["created"])

    def test_bootstraps_before_reading_full_history(self) -> None:
        self.bridge.start()
        session = self.bridge.session_for_day(
            30,
            {"title": "页面对象", "learn": "封装", "run": "pytest -q"},
        )
        self.assertTrue(session["created"])
        self.assertEqual(session["thread"]["id"], "fake-thread")
        state = json.loads((self.root / "artifacts" / "workbench-state.json").read_text(encoding="utf-8"))
        self.assertTrue(state["days"]["30"]["bootstrapped"])

    def test_recovers_an_unmaterialized_saved_thread(self) -> None:
        self.bridge.start()
        self.bridge.session_for_day(30, {"title": "页面对象"}, bootstrap=False)
        session = self.bridge.session_for_day(
            30,
            {"title": "页面对象", "learn": "封装", "run": "pytest -q"},
        )
        self.assertFalse(session["created"])
        self.assertEqual(session["thread"]["id"], "fake-thread")

    def test_replaces_a_saved_thread_when_its_rollout_is_missing(self) -> None:
        state_path = self.root / "artifacts" / "workbench-state.json"
        state_path.write_text(
            json.dumps(
                {
                    "days": {
                        "30": {
                            "thread_id": "missing-thread",
                            "created_at": "2026-08-24T00:00:00Z",
                            "bootstrapped": False,
                        }
                    }
                }
            ),
            encoding="utf-8",
        )
        self.bridge.start()

        session = self.bridge.session_for_day(
            30,
            {"title": "页面对象", "learn": "封装", "run": "pytest -q"},
        )

        self.assertTrue(session["created"])
        self.assertEqual(session["thread_id"], "fake-thread")
        state = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(state["days"]["30"]["thread_id"], "fake-thread")
        self.assertEqual(state["days"]["30"]["replaced_thread_id"], "missing-thread")
        self.assertTrue(state["days"]["30"]["bootstrapped"])

    def test_streams_turn_events(self) -> None:
        self.bridge.start()
        session = self.bridge.session_for_day(30, {"title": "页面对象"}, bootstrap=False)
        baseline = max((event["seq"] for event in self.bridge.events_after(0, timeout=0)), default=0)
        self.bridge.start_turn(session["thread_id"], "解释页面对象")
        deadline = time.monotonic() + 2
        events = []
        while time.monotonic() < deadline:
            events.extend(self.bridge.events_after(baseline, timeout=0.1))
            if any(event["method"] == "turn/completed" for event in events):
                break
            if events:
                baseline = max(event["seq"] for event in events)
        methods = {event["method"] for event in events}
        self.assertIn("item/agentMessage/delta", methods)
        self.assertIn("turn/completed", methods)

    def test_requires_explicit_approval_decision(self) -> None:
        self.bridge.start()
        session = self.bridge.session_for_day(30, {"title": "页面对象"}, bootstrap=False)
        self.bridge.start_turn(session["thread_id"], "approval")
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline and not self.bridge.status()["pending_approvals"]:
            time.sleep(0.02)
        approvals = self.bridge.status()["pending_approvals"]
        self.assertEqual(approvals[0]["request_id"], 900)
        result = self.bridge.resolve_approval(900, "accept")
        self.assertEqual(result["decision"], "accept")

    def test_rejects_unknown_approval_decision(self) -> None:
        with self.assertRaises(bridge_module.CodexProtocolError):
            self.bridge.resolve_approval(1, "alwaysAllowEverything")


if __name__ == "__main__":
    unittest.main()
