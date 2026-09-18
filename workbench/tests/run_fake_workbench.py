"""Run the workbench against the fake Codex process for visual QA."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


WORKBENCH = Path(__file__).resolve().parents[1]
PROJECT = Path(r"D:\qa-automation-learning")
sys.path.insert(0, str(WORKBENCH))

import codex_bridge  # noqa: E402
import server  # noqa: E402


FAKE = Path(__file__).resolve().parent / "fake_app_server.py"


def fake_process_factory(_args, **kwargs):
    return subprocess.Popen([sys.executable, str(FAKE)], **kwargs)


def main() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        workbench_server = server.WorkbenchServer(("127.0.0.1", 8767), server.WorkbenchHandler)
        workbench_server.project_root = PROJECT
        workbench_server.static_root = WORKBENCH / "static"
        workbench_server.codex = codex_bridge.CodexBridge(
            PROJECT,
            executable=Path(sys.executable),
            process_factory=fake_process_factory,
            request_timeout=3,
        )
        workbench_server.codex._state_path = Path(temporary) / "workbench-state.json"
        print("Fake workbench: http://127.0.0.1:8767")
        try:
            workbench_server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            workbench_server.codex.stop()
            workbench_server.server_close()


if __name__ == "__main__":
    main()
