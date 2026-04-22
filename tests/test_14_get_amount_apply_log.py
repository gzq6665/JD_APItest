from __future__ import annotations

import pytest

from utils.data_loader import build_case_ids, load_test_cases


CASES = load_test_cases("data/test_14_get_amount_apply_log.json")


@pytest.mark.parametrize(
    "case_data,get_amount_apply_log_response",
    [(case, case) for case in CASES],
    ids=build_case_ids(CASES),
    indirect=["get_amount_apply_log_response"],
)
def test_get_amount_apply_log(case_data, get_amount_apply_log_response) -> None:
    """参数化验证查看额度申请记录接口。"""

    json_data = get_amount_apply_log_response.json()
    assert case_data["expected"]["expected_status_code"] == get_amount_apply_log_response.status_code
    assert case_data["expected"]["expected_text"] in get_amount_apply_log_response.text
    assert case_data["expected"]["expected_approval_text"] in get_amount_apply_log_response.text
    assert case_data["expected"]["expected_status"] == json_data["status"]
