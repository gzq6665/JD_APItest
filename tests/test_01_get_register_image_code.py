from __future__ import annotations

import pytest

from utils.data_loader import build_case_ids, load_test_cases


CASES = load_test_cases("data/test_01_get_register_image_code.json")


@pytest.mark.parametrize(
    "case_data,register_image_code_response",
    [(case, case) for case in CASES],
    ids=build_case_ids(CASES),
    indirect=["register_image_code_response"],
)
def test_get_register_image_code(case_data, register_image_code_response) -> None:
    """参数化验证获取注册图片验证码接口。"""

    assert case_data["expected"]["expected_status_code"] == register_image_code_response.status_code
