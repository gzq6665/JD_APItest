from __future__ import annotations

import pytest

from utils.data_loader import build_case_ids, load_test_cases


CASES = load_test_cases("data/test_06_approve_realname.json")


@pytest.mark.parametrize(
    "case_data,approve_realname_response",
    [(case, case) for case in CASES],
    ids=build_case_ids(CASES),
    indirect=["approve_realname_response"],
)
def test_approve_realname(case_data, approve_realname_response) -> None:
    """参数化验证实名认证接口。"""

    assert case_data["expected"]["expected_status_code"] == approve_realname_response.status_code
    assert case_data["expected"]["expected_text"] in approve_realname_response.text
    if "expected_status" in case_data["expected"]:
        json_data = approve_realname_response.json()
        assert case_data["expected"]["expected_status"] == json_data["status"]
