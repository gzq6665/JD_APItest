from __future__ import annotations

import pytest

from utils.data_loader import build_case_ids, load_test_cases


CASES = load_test_cases("data/test_05_is_login.json")


@pytest.mark.parametrize(
    "case_data,is_login_response",
    [(case, case) for case in CASES],
    ids=build_case_ids(CASES),
    indirect=["is_login_response"],
)
def test_is_login(case_data, is_login_response) -> None:
    """参数化验证是否登录接口。"""

    json_data = is_login_response.json()
    assert case_data["expected"]["expected_status_code"] == is_login_response.status_code
    assert case_data["expected"]["expected_text"] in is_login_response.text
    assert case_data["expected"]["expected_status"] == json_data["status"]
