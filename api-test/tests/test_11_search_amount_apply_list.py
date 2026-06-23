from __future__ import annotations

import pytest

from utils.data_loader import build_case_ids, load_test_cases


CASES = load_test_cases("data/test_11_search_amount_apply_list.json")


@pytest.mark.parametrize(
    "case_data,search_amount_apply_list_response",
    [(case, case) for case in CASES],
    ids=build_case_ids(CASES),
    indirect=["search_amount_apply_list_response"],
)
def test_search_amount_apply_list(case_data, search_amount_apply_list_response) -> None:
    """参数化验证搜索额度申请列表接口。"""

    json_data = search_amount_apply_list_response.json()
    assert case_data["expected"]["expected_status_code"] == search_amount_apply_list_response.status_code
    assert case_data["expected"]["expected_text"] in search_amount_apply_list_response.text
    assert case_data["expected"]["expected_status"] == json_data["status"]
