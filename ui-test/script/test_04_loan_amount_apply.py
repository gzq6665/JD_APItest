"""Loan amount apply test cases (execution and assertions only)."""

from __future__ import annotations

from typing import Any

import allure
import pytest


@pytest.mark.loan_amount_apply
@allure.feature("Borrow Account Module")
@allure.story("Loan Amount Apply")
class TestLoanAmountApply:
    """Loan amount apply test suite."""

    @staticmethod
    def assert_equals(actual_text: str, expected_text: str) -> None:
        """Assert that the actual text equals the expected text."""
        assert actual_text == expected_text, f"Assertion failed. expected={expected_text}, actual={actual_text}"

    def test_apply_amount(
        self,
        loan_amount_apply_case_data: dict[str, Any],
        loan_amount_apply_page,
        logger,
    ) -> None:
        """Run one loan amount apply scenario based on parametrized case data."""
        allure.dynamic.title(
            f"{loan_amount_apply_case_data['case_id']} - {loan_amount_apply_case_data['title']}"
        )

        with allure.step("Open loan amount apply page"):
            loan_amount_apply_page.open_apply_page()
            previous_record_text = loan_amount_apply_page.get_latest_record_text()

        with allure.step("Submit loan amount apply form"):
            loan_amount_apply_page.submit_application(
                apply_type=loan_amount_apply_case_data["apply_type"],
                amount_account=loan_amount_apply_case_data["amount_account"] or "",
                remark=loan_amount_apply_case_data["remark"] or "",
                verifycode=loan_amount_apply_case_data["verifycode"] or "",
            )
            loan_amount_apply_page.wait_feedback()

        if loan_amount_apply_case_data["expect_result"] == "success":
            with allure.step("Assert latest application record"):
                loan_amount_apply_page.wait_latest_record_updated(previous_record_text, timeout=10)
                latest_type = loan_amount_apply_page.get_latest_record_type()
                latest_amount = loan_amount_apply_page.get_latest_record_amount()
                latest_status = loan_amount_apply_page.get_latest_record_status()
                logger.info(
                    "Loan amount apply latest record: type=%s, amount=%s, status=%s",
                    latest_type,
                    latest_amount,
                    latest_status,
                )
                self.assert_equals(latest_type, loan_amount_apply_case_data["expect_type_text"])
                self.assert_equals(latest_amount, loan_amount_apply_case_data["expect_amount_text"])
                self.assert_equals(latest_status, loan_amount_apply_case_data["expect_status_text"])
            return

        with allure.step("Assert validation text"):
            feedback_text = loan_amount_apply_page.get_error_text()
            logger.info("Loan amount apply feedback: %s", feedback_text)
            self.assert_equals(feedback_text, loan_amount_apply_case_data["expect_text"])
