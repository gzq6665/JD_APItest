from __future__ import annotations

import pytest

from utils.data_loader import build_case_ids, load_test_cases


CASES = load_test_cases("data/test_03_register.json")


@pytest.mark.parametrize(
    "case_data,register_response",
    [(case, case) for case in CASES],
    ids=build_case_ids(CASES),
    indirect=["register_response"],
)
def test_register(case_data, register_response) -> None:
    """参数化验证注册接口。"""

    json_data = register_response.json()
    assert case_data["expected"]["expected_status_code"] == register_response.status_code
    assert case_data["expected"]["expected_text"] in register_response.text
    assert case_data["expected"]["expected_status"] == json_data["status"]
