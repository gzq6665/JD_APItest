from __future__ import annotations

import pytest

from utils.data_loader import build_case_ids, load_test_cases


CASES = load_test_cases("data/test_02_send_sms.json")


@pytest.mark.parametrize(
    "case_data,send_sms_response",
    [(case, case) for case in CASES],
    ids=build_case_ids(CASES),
    indirect=["send_sms_response"],
)
def test_send_sms(case_data, send_sms_response) -> None:
    """参数化验证获取短信验证码接口。"""

    json_data = send_sms_response.json()
    assert case_data["expected"]["expected_status_code"] == send_sms_response.status_code
    assert case_data["expected"]["expected_text"] in send_sms_response.text
    assert case_data["expected"]["expected_status"] == json_data["status"]
