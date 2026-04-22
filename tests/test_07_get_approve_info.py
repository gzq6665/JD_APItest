from __future__ import annotations

import pytest

from utils.context import TestContext
from utils.data_loader import build_case_ids, load_test_cases


CASES = load_test_cases("data/test_07_get_approve_info.json")


@pytest.mark.parametrize(
    "case_data,get_approve_info_response",
    [(case, case) for case in CASES],
    ids=build_case_ids(CASES),
    indirect=["get_approve_info_response"],
)
def test_get_approve_info(case_data, get_approve_info_response, test_context: TestContext) -> None:
    """参数化验证获取认证信息接口。"""

    json_data = get_approve_info_response.json()
    card_id = str(json_data.get("card_id", ""))
    realname = str(json_data.get("realname", ""))
    assert case_data["expected"]["expected_status_code"] == get_approve_info_response.status_code
    assert test_context.card_id[:3] in card_id
    assert test_context.card_id[-3:] in card_id
    assert "*" in card_id
    assert test_context.realname[:1] in realname
    assert "*" in realname
