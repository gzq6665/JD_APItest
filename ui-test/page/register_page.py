"""Register page object (locators + page actions)."""

from __future__ import annotations

import time

from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from base.base_page import BasePage
from config import CENTER_URL, REGISTER_URL


class RegisterPage(BasePage):
    """Encapsulates interactions on the register page."""

    REGISTER_URL = REGISTER_URL
    CENTER_URL = CENTER_URL

    # Page element locators.
    PHONE_INPUT = (By.ID, "phone")
    PASSWORD_INPUT = (By.ID, "password")
    IMAGE_CODE_INPUT = (By.ID, "verifycode")
    SMS_CODE_INPUT = (By.ID, "phone_code")
    GET_SMS_CODE_BUTTON = (By.ID, "get_phone_code")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "#reg_form input.lg-btn[type='submit']")

    SUCCESS_PANEL = (By.ID, "step3")
    SUCCESS_TITLE = (By.CSS_SELECTOR, "#step3 h1")
    RETURN_CENTER_LINK = (By.CSS_SELECTOR, "a[href='/member/member/center'], a[href='member/member/center']")
    ERROR_TEXTS = (By.CSS_SELECTOR, "span.error")
    LAYER_MESSAGE = (By.CSS_SELECTOR, ".layui-layer-content")
    LAYER_MESSAGE_ALT = (By.CSS_SELECTOR, ".xubox_msg")
    SHADE_NEW = (By.CSS_SELECTOR, ".layui-layer-shade")
    SHADE_OLD = (By.CSS_SELECTOR, ".xubox_shade")

    def open_register(self) -> None:
        """Open register page URL."""
        self.open(self.REGISTER_URL)

    def input_phone(self, phone: str) -> None:
        """Input phone number."""
        self.input_text(self.PHONE_INPUT, phone)

    def input_password(self, password: str) -> None:
        """Input login password."""
        self.input_text(self.PASSWORD_INPUT, password)

    def input_image_code(self, image_code: str) -> None:
        """Input image captcha."""
        self.input_text(self.IMAGE_CODE_INPUT, image_code)

    def input_sms_code(self, sms_code: str) -> None:
        """Input SMS captcha."""
        self.input_text(self.SMS_CODE_INPUT, sms_code)

    def click_get_sms_code(self) -> None:
        """Click the SMS code send button."""
        self.click(self.GET_SMS_CODE_BUTTON)
        self.wait_shade_invisible()

    def click_submit(self) -> None:
        """Click register submit button."""
        self.wait_shade_invisible()
        submit = self.wait_clickable(self.SUBMIT_BUTTON, timeout=10)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit)
        try:
            submit.click()
        except ElementClickInterceptedException:
            self.wait_shade_invisible(timeout=10)
            self.driver.execute_script("arguments[0].click();", submit)

    def register(
        self,
        phone: str,
        password: str,
        image_code: str,
        sms_code: str,
        send_sms: bool = False,
    ) -> None:
        """Perform register submit flow."""
        self.input_phone(phone)
        self.input_password(password)
        self.input_image_code(image_code)
        if send_sms:
            self.click_get_sms_code()
        self.input_sms_code(sms_code)
        self.click_submit()

    def wait_shade_invisible(self, timeout: int = 8) -> None:
        """Wait until popup shade overlays are not visible."""
        wait = WebDriverWait(self.driver, timeout)
        for locator in (self.SHADE_NEW, self.SHADE_OLD):
            try:
                wait.until(ec.invisibility_of_element_located(locator))
            except TimeoutException:
                # Keep moving; some pages use only one overlay implementation.
                pass

    def wait_feedback(self, timeout: int = 6) -> None:
        """Wait for success area or error message to appear after submit."""
        end_time = time.time() + timeout
        while time.time() < end_time:
            if self.is_visible(self.SUCCESS_PANEL, timeout=1):
                return
            if self.get_error_text():
                return
            time.sleep(0.2)

    def get_error_text(self) -> str:
        """Get visible register error text from form validation or popup."""
        popup_msg = self.get_text(self.LAYER_MESSAGE, timeout=1) or self.get_text(self.LAYER_MESSAGE_ALT, timeout=1)
        if popup_msg:
            return popup_msg

        elements = self.driver.find_elements(*self.ERROR_TEXTS)
        texts = [element.text.strip() for element in elements if element.text and element.text.strip()]
        if texts:
            return " | ".join(texts)
        return ""

    def get_success_text(self) -> str:
        """Get visible register success text."""
        if self.is_visible(self.SUCCESS_PANEL, timeout=2):
            return self.get_text(self.SUCCESS_PANEL, timeout=2)
        return self.get_page_text()

    def get_success_title_text(self) -> str:
        """Get the exact success title text from the register success panel."""
        return self.get_text(self.SUCCESS_TITLE, timeout=2)

    def go_to_user_center(self) -> None:
        """Go to user center after register success."""
        self.wait_feedback(timeout=8)
        if self.is_visible(self.RETURN_CENTER_LINK, timeout=3):
            self.click(self.RETURN_CENTER_LINK)
            return
        self.open(self.CENTER_URL)
