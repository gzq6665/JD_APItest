from __future__ import annotations

import pytest

from utils.data_loader import build_case_ids, load_test_cases


CASES = load_test_cases("data/test_08_open_account.json")


@pytest.mark.parametrize(
    "case_data,open_account_response",
    [(case, case) for case in CASES],
    ids=build_case_ids(CASES),
    indirect=["open_account_response"],
)
def test_open_account(case_data, open_account_response) -> None:
    """参数化验证开户接口。"""

    assert case_data["expected"]["expected_status_code"] == open_account_response.status_code
