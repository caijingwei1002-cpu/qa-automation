"""加载并验证 Restful Booker JSON Schema。"""

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


SCHEMA_PATH = (
    Path(__file__).resolve().parents[1]
    / "schemas"
    / "booking.json"
)

with SCHEMA_PATH.open(encoding="utf-8") as schema_file:
    BOOKING_SCHEMA = json.load(schema_file)

# 先验证 Schema 文件本身没有写错。
Draft202012Validator.check_schema(BOOKING_SCHEMA)

VALIDATOR = Draft202012Validator(
    BOOKING_SCHEMA,
    format_checker=FormatChecker(),
)


def _validator_for(schema_key=None):
    """构造根 Schema 或指定 $defs 分支的验证器。"""
    if schema_key is None:
        return VALIDATOR

    if schema_key not in BOOKING_SCHEMA["$defs"]:
        raise ValueError(f"Unknown booking schema key: {schema_key!r}")

    selected_schema = {
        "$schema": BOOKING_SCHEMA["$schema"],
        "$defs": BOOKING_SCHEMA["$defs"],
        "$ref": f"#/$defs/{schema_key}",
    }

    return Draft202012Validator(
        selected_schema,
        format_checker=FormatChecker(),
    )


def assert_schema_valid(instance, context, *, schema_key=None):
    """断言响应符合 booking Schema，并输出可定位的路径信息。"""
    validator = _validator_for(schema_key)
    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: list(error.absolute_path),
    )

    if not errors:
        return

    details = []
    for error in errors:
        path = ".".join(str(part) for part in error.absolute_path)
        details.append(
            f"{path or '<root>'}: {error.message}"
        )

    raise AssertionError(
        f"{context} failed JSON Schema validation:\n"
        + "\n".join(details)
    )
