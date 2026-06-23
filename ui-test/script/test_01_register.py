"""Register test cases (execution and assertions only)."""

from __future__ import annotations

from typing import Any

import allure
import pytest


@pytest.mark.register
@allure.feature("Register Module")
@allure.story("User Register")
class TestRegister:
    """Register module test suite."""

    @staticmethod
    def assert_equals(actual_text: str, expected_text: str) -> None:
        """Assert that the actual text equals the expected text."""
        assert actual_text == expected_text, f"Assertion failed. expected={expected_text}, actual={actual_text}"

    def test_register(self, register_case_data: dict[str, Any], register_page, logger) -> None:
        """Run one register scenario based on parametrized case data."""
        allure.dynamic.title(f"{register_case_data['case_id']} - {register_case_data['title']}")

        with allure.step("Open register page"):
            register_page.open_register()

        with allure.step("Submit register"):
            register_page.register(
                phone=register_case_data["phone"] or "",
                password=register_case_data["password"] or "",
                image_code=register_case_data["image_code"] or "",
                sms_code=register_case_data["sms_code"] or "",
                send_sms=register_case_data["send_sms"],
            )

        with allure.step("Wait feedback"):
            register_page.wait_feedback()

        if register_case_data["expect_result"] == "success":
            with allure.step("Assert success title"):
                success_title = register_page.get_success_title_text()
                logger.info("Register success title: %s", success_title)
                self.assert_equals(success_title, register_case_data["expect_title_text"])
            return

        with allure.step("Assert error text"):
            error_text = register_page.get_error_text()
            logger.info("Register error text: %s", error_text)
            self.assert_equals(error_text, register_case_data["expect_text"])
