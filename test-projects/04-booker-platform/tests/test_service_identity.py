"""Service identity classifier unit tests.

Pure function + pure data only:
- no real OS/process inspection
- no real port probing
- no HTTP requests
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

import pytest


class IdentityStatus(StrEnum):
    ABSENT = "absent"
    UNKNOWN = "unknown"
    MISMATCH = "mismatch"
    MATCH = "match"


@dataclass(frozen=True)
class ServiceObservation:
    port: int
    listening: bool
    process_name: str | None = None
    command_line: str | None = None
    working_directory: str | None = None
    version_label: str | None = None
    permission_denied_fields: frozenset[str] = field(default_factory=frozenset)


_GENERIC_PROCESS_NAMES = {
    "java",
    "java.exe",
    "node",
    "node.exe",
    "python",
    "python.exe",
    "python3",
    "dotnet",
    "dotnet.exe",
}


def _normalize(value: str | None) -> str:
    return value.strip().lower() if value else ""


def _mentions_service(value: str | None, service_name: str) -> bool:
    return service_name.lower() in _normalize(value)


def _has_other_service_marker(
    value: str | None,
    expected_service: str,
) -> bool:
    """Detect explicit identity evidence for a different known service."""
    normalized = _normalize(value)

    if not normalized:
        return False

    known_services = {
        "auth",
        "room",
        "booking",
        "report",
        "message",
        "branding",
    }

    expected = expected_service.lower()

    return any(service != expected and service in normalized for service in known_services)


def classify_service_identity(
    *,
    expected_service: str,
    expected_port: int,
    observation: ServiceObservation,
) -> IdentityStatus:
    """Classify whether the listener is the expected service.

    HTTP status/result is intentionally excluded from this function.
    """
    if observation.port != expected_port:
        raise ValueError(
            f"Observation port {observation.port} does not match expected port {expected_port}"
        )

    if not observation.listening:
        return IdentityStatus.ABSENT

    strong_identity_fields = (
        observation.command_line,
        observation.working_directory,
        observation.version_label,
    )

    # Explicit contradictory evidence wins over missing evidence.
    if any(_has_other_service_marker(value, expected_service) for value in strong_identity_fields):
        return IdentityStatus.MISMATCH

    positive_evidence = any(
        _mentions_service(value, expected_service) for value in strong_identity_fields
    )

    process_name = _normalize(observation.process_name)

    if (
        process_name
        and process_name not in _GENERIC_PROCESS_NAMES
        and _mentions_service(process_name, expected_service)
    ):
        positive_evidence = True

    if positive_evidence:
        return IdentityStatus.MATCH

    # A listener exists, but identity cannot be established.
    return IdentityStatus.UNKNOWN


@pytest.mark.parametrize(
    (
        "case_name",
        "observation",
        "observed_http_status",
        "expected_status",
    ),
    [
        (
            "absent_no_listener",
            ServiceObservation(
                port=3001,
                listening=False,
            ),
            None,
            IdentityStatus.ABSENT,
        ),
        (
            "match_strong_identity",
            ServiceObservation(
                port=3001,
                listening=True,
                process_name="node",
                command_line="node services/room/server.js",
                working_directory=r"D:\booker-platform\services\room",
                version_label="room-service 1.4.2",
            ),
            None,
            IdentityStatus.MATCH,
        ),
        (
            "unknown_generic_process_only",
            ServiceObservation(
                port=3001,
                listening=True,
                process_name="node",
            ),
            None,
            IdentityStatus.UNKNOWN,
        ),
        (
            "unknown_permission_denied",
            ServiceObservation(
                port=3001,
                listening=True,
                process_name="node",
                command_line=None,
                working_directory=None,
                version_label=None,
                permission_denied_fields=frozenset(
                    {
                        "command_line",
                        "working_directory",
                        "version_label",
                    }
                ),
            ),
            None,
            IdentityStatus.UNKNOWN,
        ),
        (
            "mismatch_other_service",
            ServiceObservation(
                port=3001,
                listening=True,
                process_name="node",
                command_line="node services/booking/server.js",
                working_directory=r"D:\booker-platform\services\booking",
                version_label="booking-service 2.1.0",
            ),
            None,
            IdentityStatus.MISMATCH,
        ),
        (
            "mismatch_conflict_beats_permission_missing",
            ServiceObservation(
                port=3001,
                listening=True,
                process_name="node",
                command_line="node services/booking/server.js",
                working_directory=None,
                version_label=None,
                permission_denied_fields=frozenset(
                    {
                        "working_directory",
                        "version_label",
                    }
                ),
            ),
            None,
            IdentityStatus.MISMATCH,
        ),
        (
            "unknown_http_200_but_identity_insufficient",
            ServiceObservation(
                port=3001,
                listening=True,
                process_name="node",
                command_line=None,
                working_directory=None,
                version_label=None,
                permission_denied_fields=frozenset(
                    {
                        "command_line",
                        "working_directory",
                        "version_label",
                    }
                ),
            ),
            200,
            IdentityStatus.UNKNOWN,
        ),
        (
            "match_identity_even_if_http_500",
            ServiceObservation(
                port=3001,
                listening=True,
                process_name="node",
                command_line="node services/room/server.js",
                working_directory=r"D:\booker-platform\services\room",
                version_label="room-service 1.4.2",
            ),
            500,
            IdentityStatus.MATCH,
        ),
    ],
    ids=lambda value: value if isinstance(value, str) else None,
)
def test_classify_service_identity(
    case_name,
    observation,
    observed_http_status,
    expected_status,
):
    # HTTP is deliberately scenario metadata only.
    # It is never passed into classify_service_identity().
    _ = case_name
    _ = observed_http_status

    actual = classify_service_identity(
        expected_service="room",
        expected_port=3001,
        observation=observation,
    )

    assert actual == expected_status


def test_rejects_observation_for_wrong_port():
    observation = ServiceObservation(
        port=3005,
        listening=True,
        process_name="node",
        command_line="node services/room/server.js",
    )

    with pytest.raises(ValueError, match="does not match expected port"):
        classify_service_identity(
            expected_service="room",
            expected_port=3001,
            observation=observation,
        )
