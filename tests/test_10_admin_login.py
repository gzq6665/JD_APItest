from __future__ import annotations

import pytest

from utils.data_loader import build_case_ids, load_test_cases


CASES = load_test_cases("data/test_10_admin_login.json")


@pytest.mark.parametrize(
    "case_data,admin_login_response",
    [(case, case) for case in CASES],
    ids=build_case_ids(CASES),
    indirect=["admin_login_response"],
)
def test_admin_login(case_data, admin_login_response) -> None:
    """参数化验证后台登录接口。"""

    json_data = admin_login_response.json()
    assert case_data["expected"]["expected_status_code"] == admin_login_response.status_code
    assert case_data["expected"]["expected_text"] in admin_login_response.text
    assert case_data["expected"]["expected_status"] == json_data["status"]
