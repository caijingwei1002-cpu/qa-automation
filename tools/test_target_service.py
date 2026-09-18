from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import Mock

from tools.target_service import ensure_target_service, observe_target_service


def _definition() -> dict[str, object]:
    return {
        "kind": "git",
        "url_env": "RESTFUL_BOOKER_URL",
        "default_url": "http://127.0.0.1:3001",
        "local_directory": "restful-booker",
        "startup": {
            "command": ["npm", "start"],
            "health_path": "/ping",
            "expected_status": 201,
            "startup_timeout_seconds": 5,
            "poll_interval_seconds": 0.1,
        },
    }


def test_reuses_healthy_service_without_starting(tmp_path: Path):
    probe = Mock(return_value=(True, "http=201"))
    popen = Mock()

    result = ensure_target_service(
        "restful-booker",
        _definition(),
        target_root=tmp_path,
        probe=probe,
        popen=popen,
    )

    assert result.state == "already-running"
    assert result.ok
    popen.assert_not_called()


def test_observe_never_starts_a_service(tmp_path: Path):
    probe = Mock(return_value=(False, "ConnectionRefusedError"))

    result = observe_target_service(
        "restful-booker",
        _definition(),
        environ={},
        probe=probe,
    )

    assert result.state == "unreachable"
    assert not result.ok
    assert "未启动或修改" not in result.message
    assert "身份与产品结论均未建立" in result.message


def test_observe_reports_reachability_without_claiming_product_health(tmp_path: Path):
    probe = Mock(return_value=(True, "http=201"))

    result = observe_target_service(
        "restful-booker",
        _definition(),
        environ={},
        probe=probe,
    )

    assert result.state == "identity-match"
    assert result.ok
    assert "只读 identity signature" in result.message
    assert "未启动或修改服务" in result.message


def test_identity_signature_mismatch_never_starts_service(tmp_path: Path):
    probe = Mock(return_value=(True, "http=200"))
    popen = Mock()

    result = ensure_target_service(
        "restful-booker",
        _definition(),
        target_root=tmp_path,
        environ={},
        probe=probe,
        popen=popen,
    )

    assert result.state == "identity-mismatch"
    assert not result.ok
    popen.assert_not_called()


def test_starts_service_and_waits_until_health_check_passes(tmp_path: Path):
    (tmp_path / "restful-booker").mkdir()
    process = Mock(pid=4321)
    process.poll.return_value = None
    probe = Mock(
        side_effect=[
            (False, "ConnectionRefusedError"),
            (False, "ConnectionRefusedError"),
            (True, "http=201"),
        ]
    )
    sleep = Mock()
    popen = Mock(return_value=process)

    result = ensure_target_service(
        "restful-booker",
        _definition(),
        target_root=tmp_path,
        probe=probe,
        popen=popen,
        sleep=sleep,
        monotonic=Mock(side_effect=[0.0, 0.2, 0.4]),
    )

    assert result.state == "started"
    assert result.pid == 4321
    popen.assert_called_once()
    expected_command = "npm.cmd" if os.name == "nt" else "npm"
    assert popen.call_args.args[0][0] == expected_command
    sleep.assert_called_once_with(0.1)


def test_skips_non_local_target(tmp_path: Path):
    definition = _definition()
    definition["default_url"] = "https://staging.example.test"
    popen = Mock()

    result = ensure_target_service(
        "restful-booker",
        definition,
        target_root=tmp_path,
        environ={},
        popen=popen,
    )

    assert result.state == "skipped"
    assert "不是本地地址" in result.message
    popen.assert_not_called()
