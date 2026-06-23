"""Admin amount-apply-audit test cases (execution and assertions only)."""

from __future__ import annotations

from typing import Any

import allure
import pytest


@pytest.mark.admin_amount_apply_audit
@allure.feature("Admin Borrow Management")
@allure.story("Amount Apply Audit")
class TestAdminAmountApplyAudit:
    """Backend amount-apply-audit test suite."""

    @staticmethod
    def assert_equals(actual_text: str, expected_text: str) -> None:
        """Assert that the actual text equals the expected text."""
        assert actual_text == expected_text, f"Assertion failed. expected={expected_text}, actual={actual_text}"

    def test_admin_amount_apply_audit(
        self,
        admin_amount_apply_audit_case_data: dict[str, Any],
        prepared_admin_amount_apply_audit_context,
        logger,
    ) -> None:
        """Audit one client amount-apply record and assert the exact backend log fields."""
        allure.dynamic.title(
            f"{admin_amount_apply_audit_case_data['case_id']} - {admin_amount_apply_audit_case_data['title']}"
        )
        admin_amount_apply_audit_page = prepared_admin_amount_apply_audit_context["page"]
        fresh_pending_amount_apply = prepared_admin_amount_apply_audit_context["fresh_pending_amount_apply"]
        selected_row = prepared_admin_amount_apply_audit_context["selected_row"]
        selected_id = selected_row["id"]
        selected_category = selected_row["category"]
        selected_status = selected_row["status"]

        with allure.step("Submit audit result"):
            admin_amount_apply_audit_page.audit_selected_application(
                income_amount=admin_amount_apply_audit_case_data["income_amount"],
                audit_status_value=admin_amount_apply_audit_case_data["audit_status_value"],
                audit_remark=admin_amount_apply_audit_case_data["audit_remark"],
                captcha=admin_amount_apply_audit_case_data["captcha"],
            )

        with allure.step("Open amount apply log page"):
            admin_amount_apply_audit_page.open_amount_apply_log_page()
            admin_amount_apply_audit_page.search_audit_log(
                member_name=fresh_pending_amount_apply["phone"],
                log_status_value=admin_amount_apply_audit_case_data["log_status_value"],
            )

        with allure.step("Assert exact audit log fields"):
            log_row = admin_amount_apply_audit_page.get_row_data_by_id(selected_id)
            logger.info(
                "Admin amount apply audit log row: id=%s, category=%s, pass_amount=%s, status=%s",
                log_row["id"],
                log_row["category"],
                log_row["pass_amount"],
                log_row["status"],
            )
            self.assert_equals(selected_category, admin_amount_apply_audit_case_data["expect_category_text"])
            self.assert_equals(selected_status, "待审核")
            self.assert_equals(log_row["id"], selected_id)
            self.assert_equals(log_row["category"], admin_amount_apply_audit_case_data["expect_category_text"])
            self.assert_equals(log_row["pass_amount"], fresh_pending_amount_apply["pass_amount"])
            self.assert_equals(log_row["status"], admin_amount_apply_audit_case_data["expect_status_text"])
