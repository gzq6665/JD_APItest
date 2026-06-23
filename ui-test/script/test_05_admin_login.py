"""Admin login test cases (execution and assertions only)."""

from __future__ import annotations

from typing import Any

import allure
import pytest


@pytest.mark.admin_login
@allure.feature("Admin Login Module")
@allure.story("Backend Admin Login")
class TestAdminLogin:
    """Admin login module test suite."""

    @staticmethod
    def assert_equals(actual_text: str, expected_text: str) -> None:
        """Assert that the actual text equals the expected text."""
        assert actual_text == expected_text, f"Assertion failed. expected={expected_text}, actual={actual_text}"

    def test_admin_login(self, admin_login_case_data: dict[str, Any], admin_login_page, logger) -> None:
        """Run one backend admin login scenario based on parametrized case data."""
        allure.dynamic.title(f"{admin_login_case_data['case_id']} - {admin_login_case_data['title']}")

        with allure.step("Open backend login page"):
            admin_login_page.open_login()

        with allure.step("Submit backend login form"):
            admin_login_page.login(
                username=admin_login_case_data["username"] or "",
                password=admin_login_case_data["password"] or "",
                captcha=admin_login_case_data["captcha"] or "",
            )
            admin_login_page.wait_login_feedback()

        if admin_login_case_data["expect_result"] == "success":
            with allure.step("Assert backend home elements"):
                current_url = admin_login_page.get_current_url()
                brand_text = admin_login_page.get_brand_text()
                user_info_text = admin_login_page.get_user_info_text()
                logger.info(
                    "Admin login success elements: url=%s, brand=%s, user=%s",
                    current_url,
                    brand_text,
                    user_info_text,
                )
                self.assert_equals(current_url, admin_login_case_data["expect_url"])
                self.assert_equals(brand_text, admin_login_case_data["expect_brand_text"])
                self.assert_equals(user_info_text, admin_login_case_data["expect_user_text"])
            return

        with allure.step("Assert backend error text"):
            error_text = admin_login_page.get_error_text()
            logger.info("Admin login error text: %s", error_text)
            self.assert_equals(error_text, admin_login_case_data["expect_text"])
