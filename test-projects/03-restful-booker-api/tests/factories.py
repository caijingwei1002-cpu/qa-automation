from copy import deepcopy
from collections.abc import Mapping
from datetime import date, timedelta
from typing import Any
from uuid import uuid4


def build_booking_payload(**overrides: Any) -> dict[str, Any]:
    """构造独立、合法且带唯一标识的 booking 请求数据。"""

    # 唯一标识放在 firstname 中，避免不同测试使用相同业务数据互相干扰。
    unique_id = uuid4().hex[:8]

    # 日期使用动态未来日期，避免测试运行一段时间后基线数据过期。
    checkin = date.today() + timedelta(days=7)
    checkout = checkin + timedelta(days=3)

    # 先建立完整且合法的默认 payload，调用方只覆盖当前场景关心的字段。
    payload = {
        "firstname": f"Test{unique_id}",
        "lastname": "User",
        "totalprice": 200,
        "depositpaid": True,
        "bookingdates": {
            "checkin": checkin.isoformat(),
            "checkout": checkout.isoformat(),
        },
        "additionalneeds": "Breakfast",
    }

    # 深拷贝覆盖值，避免调用方后续修改嵌套对象时污染本次数据。
    overrides = deepcopy(overrides)

    # bookingdates 采用局部合并，覆盖 checkin 时仍保留默认 checkout。
    bookingdates_override = overrides.pop("bookingdates", None)

    payload.update(overrides)

    if bookingdates_override is not None:
        if not isinstance(bookingdates_override, Mapping):
            raise TypeError("bookingdates 覆盖值必须是对象或 Mapping")
        payload["bookingdates"].update(bookingdates_override)

    return payload
