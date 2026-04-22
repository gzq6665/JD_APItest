from __future__ import annotations

import pytest

from utils.data_loader import build_case_ids, load_test_cases


CASES = load_test_cases("data/test_12_open_amount_verify_page.json")


@pytest.mark.parametrize(
    "case_data,open_amount_verify_page_response",
    [(case, case) for case in CASES],
    ids=build_case_ids(CASES),
    indirect=["open_amount_verify_page_response"],
)
def test_open_amount_verify_page(case_data, open_amount_verify_page_response) -> None:
    """参数化验证打开额度审批页面接口。"""

    json_data = open_amount_verify_page_response.json()
    assert case_data["expected"]["expected_status_code"] == open_amount_verify_page_response.status_code
    assert case_data["expected"]["expected_text"] in open_amount_verify_page_response.text
    assert case_data["expected"]["expected_status"] == json_data["status"]
