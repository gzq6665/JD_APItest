"""Open-account page object (locators + page actions)."""

from __future__ import annotations

import time

from selenium.webdriver.common.by import By

from base.base_page import BasePage
from config import CENTER_URL, TRUST_REG_URL


class OpenAccountPage(BasePage):
    """Encapsulates interactions on the trust-account opening page."""

    CENTER_URL = CENTER_URL
    TRUST_REG_URL = TRUST_REG_URL

    CENTER_OPEN_NOW_LINK = (By.CSS_SELECTOR, "a[href='/trust/public/reg'], a[href='trust/public/reg']")
    TRUST_TITLE = (By.CSS_SELECTOR, ".reg-tit")
    INFO_FORM = (By.ID, "safeName")
    REALNAME_INPUT = (By.CSS_SELECTOR, "#safeName input[name='realname']")
    CARD_ID_INPUT = (By.CSS_SELECTOR, "#safeName input[name='card_id']")
    REALNAME_ERROR = (By.CSS_SELECTOR, "#safeName input[name='realname'] + label .validation-invalid")
    CARD_ID_ERROR = (By.CSS_SELECTOR, "#safeName input[name='card_id'] + label .validation-invalid")
    CONFIRM_SUBMIT_BUTTON = (By.CSS_SELECTOR, "#safeName input[type='submit']")
    OPEN_NOW_BUTTON = (By.CSS_SELECTOR, "#successForm input[type='button']")
    SUCCESS_INFO_TITLE = (By.CSS_SELECTOR, "#successForm .info p:first-child")
    INFO_ERROR = (By.CSS_SELECTOR, "#safeName .dy-error, #safeName label.error, #safeName .error")
    STEP_PANEL = (By.CSS_SELECTOR, ".reg-success")

    def open_open_account_page(self) -> None:
        """Open the trust-account registration page."""
        self.open(self.CENTER_URL)
        if self.is_visible(self.CENTER_OPEN_NOW_LINK, timeout=5):
            self.click_open_now_entry()
        else:
            self.open(self.TRUST_REG_URL)

        self.wait_visible(self.TRUST_TITLE, timeout=10)
        if not self.is_visible(self.INFO_FORM, timeout=3) and not self.is_ready_for_open():
            self.open(self.TRUST_REG_URL)

    def click_open_now_entry(self) -> None:
        """Click the open-now entry from user center."""
        self.click(self.CENTER_OPEN_NOW_LINK)

    def input_realname(self, realname: str) -> None:
        """Input the real name."""
        self.input_text(self.REALNAME_INPUT, realname)

    def input_card_id(self, card_id: str) -> None:
        """Input the identity-card number."""
        self.input_text(self.CARD_ID_INPUT, card_id)

    def click_confirm_submit(self) -> None:
        """Click the information submit button."""
        submit = self.wait_clickable(self.CONFIRM_SUBMIT_BUTTON, timeout=10)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit)
        self.driver.execute_script("arguments[0].click();", submit)

    def submit_identity_info(self, realname: str, card_id: str) -> None:
        """Fill the identity form and submit it."""
        self.input_realname(realname)
        self.input_card_id(card_id)
        self.click_confirm_submit()

    def click_open_now(self) -> None:
        """Click the step-3 open-now button."""
        button = self.wait_clickable(self.OPEN_NOW_BUTTON, timeout=10)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        self.driver.execute_script("arguments[0].click();", button)

    def click_open_now_and_switch(self, timeout: int = 10) -> str:
        """Click the final open-now button and switch to the external page if a new tab opens."""
        old_handles = list(self.driver.window_handles)
        self.click_open_now()

        end_time = time.time() + timeout
        while time.time() < end_time:
            current_handles = self.driver.window_handles
            new_handles = [handle for handle in current_handles if handle not in old_handles]
            if new_handles:
                self.driver.switch_to.window(new_handles[-1])
                time.sleep(1)
                return self.get_current_url()

            current_url = self.get_current_url()
            if self.is_external_register_page(current_url):
                return current_url
            time.sleep(0.2)

        return self.get_current_url()

    @staticmethod
    def is_external_register_page(url: str) -> bool:
        """Check whether the current page has jumped to the external trust-host page."""
        return "121.43.169.97:8000" in url or "muser/publicRequests" in url

    def close_external_and_back(self) -> None:
        """Close the external trust page and switch back to the original window when needed."""
        if len(self.driver.window_handles) <= 1:
            return

        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def wait_feedback(self, timeout: int = 8) -> None:
        """Wait until validation error or step-3 panel is visible."""
        end_time = time.time() + timeout
        while time.time() < end_time:
            if self.get_error_text():
                return
            if self.is_ready_for_open():
                return
            time.sleep(0.2)

    def is_ready_for_open(self) -> bool:
        """Check whether the page has switched to the final open-now step."""
        return self.is_visible(self.OPEN_NOW_BUTTON, timeout=2) or self.is_visible(self.STEP_PANEL, timeout=2)

    def get_error_text(self) -> str:
        """Get visible validation or business error text."""
        realname_error = self.get_realname_error_text()
        if realname_error:
            return realname_error

        card_id_error = self.get_card_id_error_text()
        if card_id_error:
            return card_id_error

        elements = self.driver.find_elements(*self.INFO_ERROR)
        texts = [element.text.strip() for element in elements if element.text and element.text.strip()]
        if texts:
            return " | ".join(texts)
        return ""

    def get_success_text(self) -> str:
        """Get visible text from the step-3 open-now panel."""
        if self.is_ready_for_open():
            return self.get_page_text()
        return ""

    def get_realname_error_text(self) -> str:
        """Get the exact real-name validation text."""
        return self.get_text(self.REALNAME_ERROR, timeout=2)

    def get_card_id_error_text(self) -> str:
        """Get the exact ID-card validation text."""
        return self.get_text(self.CARD_ID_ERROR, timeout=2)

    def get_open_now_button_text(self) -> str:
        """Get the exact button value shown on the final open-account step."""
        if not self.is_visible(self.OPEN_NOW_BUTTON, timeout=2):
            return ""
        return self.find(self.OPEN_NOW_BUTTON).get_attribute("value").strip()

    def get_success_info_title_text(self) -> str:
        """Get the exact success info title shown before the external redirect step."""
        return self.get_text(self.SUCCESS_INFO_TITLE, timeout=2)
