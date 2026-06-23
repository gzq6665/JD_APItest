"""Login test cases (execution and assertions only)."""

from __future__ import annotations

from typing import Any

import allure
import pytest


@pytest.mark.login
@allure.feature("Login Module")
@allure.story("User Login")
class TestLogin:
    """Login module test suite."""

    @staticmethod
    def assert_equals(actual_text: str, expected_text: str) -> None:
        """Assert that the actual text equals the expected text."""
        assert actual_text == expected_text, f"Assertion failed. expected={expected_text}, actual={actual_text}"

    def test_login(self, case_data: dict[str, Any], login_page, logger) -> None:
        """Run one login scenario based on parametrized case data."""
        allure.dynamic.title(f"{case_data['case_id']} - {case_data['title']}")

        with allure.step("Open login page"):
            login_page.open_login()

        if case_data["need_captcha"]:
            with allure.step("Trigger captcha display"):
                triggered = login_page.trigger_captcha(
                    case_data["valid_username"],
                    case_data["valid_password"],
                )
                if not triggered:
                    pytest.skip("Captcha was not triggered in current environment.")

        with allure.step("Submit login"):
            login_page.login(
                username=case_data["username"] or "",
                password=case_data["password"] or "",
                captcha=case_data["captcha"],
            )
            login_page.wait_login_feedback()

        if case_data["expect_result"] == "success":
            with allure.step("Assert success elements"):
                logout_text = login_page.get_logout_text()
                user_text = login_page.get_user_info_text()
                logger.info("Login success elements: logout=%s, user=%s", logout_text, user_text)
                self.assert_equals(logout_text, case_data["expect_logout_text"])
                self.assert_equals(user_text, case_data["expect_user_text"])
            return

        with allure.step("Assert error text"):
            error_text = login_page.get_error_text()
            logger.info("Error text: %s", error_text)
            self.assert_equals(error_text, case_data["expect_text"])
