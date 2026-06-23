"""Open-account test cases (execution and assertions only)."""

from __future__ import annotations

from typing import Any

import allure
import pytest


@pytest.mark.open_account
@allure.feature("Trust Account Module")
@allure.story("Open Account")
class TestOpenAccount:
    """Open-account module test suite."""

    @staticmethod
    def assert_equals(actual_text: str, expected_text: str) -> None:
        """Assert that the actual text equals the expected text."""
        assert actual_text == expected_text, f"Assertion failed. expected={expected_text}, actual={actual_text}"

    def test_open_account(
        self,
        open_account_case_data: dict[str, Any],
        open_account_page,
        logger,
    ) -> None:
        """Run one open-account scenario based on parametrized case data."""
        allure.dynamic.title(f"{open_account_case_data['case_id']} - {open_account_case_data['title']}")

        with allure.step("Open trust-account registration page"):
            open_account_page.open_open_account_page()

        with allure.step("Submit identity information"):
            open_account_page.submit_identity_info(
                realname=open_account_case_data["realname"] or "",
                card_id=open_account_case_data["card_id"] or "",
            )
            open_account_page.wait_feedback()

        if open_account_case_data["expect_result"] == "success":
            with allure.step("Assert step-3 success elements"):
                info_title = open_account_page.get_success_info_title_text()
                button_text = open_account_page.get_open_now_button_text()
                logger.info("Open account success elements: info_title=%s, button=%s", info_title, button_text)
                self.assert_equals(info_title, open_account_case_data["expect_info_title_text"])
                self.assert_equals(button_text, open_account_case_data["expect_button_text"])

            with allure.step("Click open-now button and assert external page"):
                redirect_url = open_account_page.click_open_now_and_switch()
                logger.info("Open account redirect url: %s", redirect_url)
                self.assert_equals(redirect_url, open_account_case_data["expect_redirect_url"])
                open_account_page.close_external_and_back()
            return

        with allure.step("Assert validation text"):
            if open_account_case_data["expect_error_field"] == "realname":
                error_text = open_account_page.get_realname_error_text()
            else:
                error_text = open_account_page.get_card_id_error_text()
            logger.info("Open account error text: %s", error_text)
            self.assert_equals(error_text, open_account_case_data["expect_text"])
