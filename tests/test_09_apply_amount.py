from __future__ import annotations

import pytest

from utils.data_loader import build_case_ids, load_test_cases


CASES = load_test_cases("data/test_09_apply_amount.json")


@pytest.mark.parametrize(
    "case_data,apply_amount_response",
    [(case, case) for case in CASES],
    ids=build_case_ids(CASES),
    indirect=["apply_amount_response"],
)
def test_apply_amount(case_data, apply_amount_response) -> None:
    """参数化验证申请额度接口。"""

    json_data = apply_amount_response.json()
    assert case_data["expected"]["expected_status_code"] == apply_amount_response.status_code
    assert case_data["expected"]["expected_text"] in apply_amount_response.text
    assert case_data["expected"]["expected_status"] == json_data["status"]
