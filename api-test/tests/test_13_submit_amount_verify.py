from __future__ import annotations

import pytest

from utils.data_loader import build_case_ids, load_test_cases


CASES = load_test_cases("data/test_13_submit_amount_verify.json")


@pytest.mark.parametrize(
    "case_data,submit_amount_verify_response",
    [(case, case) for case in CASES],
    ids=build_case_ids(CASES),
    indirect=["submit_amount_verify_response"],
)
def test_submit_amount_verify(case_data, submit_amount_verify_response) -> None:
    """参数化验证进行额度审批接口。"""

    json_data = submit_amount_verify_response.json()
    assert case_data["expected"]["expected_status_code"] == submit_amount_verify_response.status_code
    assert case_data["expected"]["expected_text"] in submit_amount_verify_response.text
    assert case_data["expected"]["expected_status"] == json_data["status"]
