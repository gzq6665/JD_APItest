"""Loan amount apply page object (locators + page actions)."""

from __future__ import annotations

import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from base.base_page import BasePage
from config import CENTER_URL, LOAN_AMOUNT_APPLY_URL


class LoanAmountApplyPage(BasePage):
    """Encapsulates interactions on the loan amount apply page."""

    CENTER_URL = CENTER_URL
    LOAN_AMOUNT_APPLY_URL = LOAN_AMOUNT_APPLY_URL

    BORROW_ACCOUNT_LINK = (By.CSS_SELECTOR, "a[href*='user_role=1']")
    APPLY_AMOUNT_MENU = (By.CSS_SELECTOR, "dd a[href*='loan/amount/index']")
    APPLY_TITLE = (By.CSS_SELECTOR, ".tips-hd h2")
    APPLY_FORM = (By.ID, "mamountapply")
    APPLY_TYPE_RADIOS = (By.CSS_SELECTOR, "#mamountapply input[name='amount_type']")
    AMOUNT_INPUT = (By.ID, "amount_account")
    REMARK_TEXTAREA = (By.CSS_SELECTOR, "#mamountapply textarea[name='remark']")
    VERIFYCODE_INPUT = (By.CSS_SELECTOR, "#mamountapply input[name='verifycode']")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "#mamountapply input[type='submit']")
    FORM_ERRORS = (By.CSS_SELECTOR, "#mamountapply label.error")
    LAYER_MESSAGE = (By.CSS_SELECTOR, ".layui-layer-content")
    LAYER_MESSAGE_ALT = (By.CSS_SELECTOR, ".xubox_msg")
    RECORD_ROWS = (By.CSS_SELECTOR, "#amount_list tr")
    LATEST_RECORD_ROW = (By.CSS_SELECTOR, "#amount_list tr:first-child")
    LATEST_RECORD_TYPE = (By.CSS_SELECTOR, "#amount_list tr:first-child td:nth-child(2)")
    LATEST_RECORD_AMOUNT = (By.CSS_SELECTOR, "#amount_list tr:first-child td:nth-child(3)")
    LATEST_RECORD_STATUS = (By.CSS_SELECTOR, "#amount_list tr:first-child td:nth-child(6)")

    def open_apply_page(self) -> None:
        """Open the apply amount page from the logged-in user area."""
        self.open(self.CENTER_URL)
        if self.is_visible(self.BORROW_ACCOUNT_LINK, timeout=5):
            self.click_borrow_account()
            try:
                self.wait_visible(self.APPLY_AMOUNT_MENU, timeout=5)
                self.click_apply_amount_menu()
            except TimeoutException:
                pass

        if not self.is_visible(self.APPLY_FORM, timeout=3):
            self.open(self.LOAN_AMOUNT_APPLY_URL)

        self.wait_visible(self.APPLY_TITLE, timeout=10)
        self.wait_visible(self.APPLY_FORM, timeout=10)

    def click_borrow_account(self) -> None:
        """Click the borrow-account role switch entry."""
        self.click(self.BORROW_ACCOUNT_LINK)

    def click_apply_amount_menu(self) -> None:
        """Click the apply amount entry in the left menu."""
        self.click(self.APPLY_AMOUNT_MENU)

    def choose_apply_type(self, apply_type: str | None = None) -> None:
        """Choose an application type radio item."""
        radios = self.driver.find_elements(*self.APPLY_TYPE_RADIOS)
        if not radios:
            return

        target_radio = None
        if apply_type and apply_type != "first":
            for radio in radios:
                if radio.get_attribute("value") == apply_type:
                    target_radio = radio
                    break
        if target_radio is None:
            target_radio = radios[0]

        self.driver.execute_script("arguments[0].click();", target_radio)

    def input_amount(self, amount_account: str) -> None:
        """Input the requested amount."""
        self.input_text(self.AMOUNT_INPUT, amount_account)

    def input_remark(self, remark: str) -> None:
        """Input the detail remark."""
        self.input_text(self.REMARK_TEXTAREA, remark)

    def input_verifycode(self, verifycode: str) -> None:
        """Input the image captcha."""
        self.input_text(self.VERIFYCODE_INPUT, verifycode)

    def click_submit(self) -> None:
        """Click the submit button."""
        submit = self.wait_clickable(self.SUBMIT_BUTTON, timeout=10)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit)
        self.driver.execute_script("arguments[0].click();", submit)

    def submit_application(
        self,
        amount_account: str,
        remark: str,
        verifycode: str,
        apply_type: str | None = "first",
    ) -> None:
        """Fill the form and submit the loan amount apply request."""
        self.choose_apply_type(apply_type)
        self.input_amount(amount_account)
        self.input_remark(remark)
        self.input_verifycode(verifycode)
        self.click_submit()

    def wait_feedback(self, timeout: int = 6) -> None:
        """Wait for validation or submit feedback after submit."""
        end_time = time.time() + timeout
        while time.time() < end_time:
            if self.get_error_text():
                return
            if self.get_success_text():
                return
            time.sleep(0.2)

    def get_error_text(self) -> str:
        """Get visible form validation text or popup message."""
        popup_msg = self.get_text(self.LAYER_MESSAGE, timeout=1) or self.get_text(self.LAYER_MESSAGE_ALT, timeout=1)
        if popup_msg:
            return popup_msg

        elements = self.driver.find_elements(*self.FORM_ERRORS)
        texts = [element.text.strip() for element in elements if element.text and element.text.strip()]
        if texts:
            return " | ".join(texts)
        return ""

    def get_success_text(self) -> str:
        """Get visible submit success message."""
        return self.get_text(self.LAYER_MESSAGE, timeout=1) or self.get_text(self.LAYER_MESSAGE_ALT, timeout=1)

    def get_latest_record_text(self) -> str:
        """Get the visible text of the latest application record row."""
        return self.get_text(self.LATEST_RECORD_ROW, timeout=2)

    def wait_latest_record_updated(self, previous_text: str, timeout: int = 10) -> None:
        """Wait until the latest record row changes after a successful submit."""
        end_time = time.time() + timeout
        while time.time() < end_time:
            latest_text = self.get_latest_record_text()
            if latest_text and latest_text != previous_text:
                return
            time.sleep(0.2)

    def get_latest_record_type(self) -> str:
        """Get the type text from the latest application record row."""
        return self.get_text(self.LATEST_RECORD_TYPE, timeout=2)

    def get_latest_record_amount(self) -> str:
        """Get the amount text from the latest application record row."""
        return self.get_text(self.LATEST_RECORD_AMOUNT, timeout=2)

    def get_latest_record_status(self) -> str:
        """Get the status text from the latest application record row."""
        return self.get_text(self.LATEST_RECORD_STATUS, timeout=2)
